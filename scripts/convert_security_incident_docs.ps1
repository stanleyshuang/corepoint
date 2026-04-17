$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.IO.Compression.FileSystem

$SourceDir = Join-Path $PSScriptRoot '..\tmp\事件處理程序書'
$OutputDir = Join-Path $PSScriptRoot '..\logs\security_incident_response_procedures'

function Get-InnerText {
    param(
        [Parameter(Mandatory = $true)]
        [System.Xml.XmlNode]$Node,
        [Parameter(Mandatory = $true)]
        [System.Xml.XmlNamespaceManager]$Ns
    )

    $parts = @()
    foreach ($textNode in $Node.SelectNodes('.//w:t', $Ns)) {
        $parts += [string]$textNode.InnerText
    }
    $text = ($parts -join '')
    $text = $text -replace '\s+', ' '
    return $text.Trim()
}

function Escape-MarkdownCell {
    param([string]$Text)
    if ($null -eq $Text) { return '' }
    $escaped = $Text.Replace('|', '\|')
    return ($escaped -replace "(`r`n|`n|`r)", '<br>')
}

function Get-SafeFileName {
    param([string]$Name)
    $safe = $Name
    foreach ($char in [System.IO.Path]::GetInvalidFileNameChars()) {
        $safe = $safe.Replace($char, '_')
    }
    return $safe
}

function Read-ZipXml {
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.Compression.ZipArchive]$Zip,
        [Parameter(Mandatory = $true)]
        [string]$EntryPath
    )

    $entry = $Zip.Entries | Where-Object { $_.FullName -eq $EntryPath } | Select-Object -First 1
    if (-not $entry) {
        throw "Missing zip entry: $EntryPath"
    }

    $stream = $entry.Open()
    try {
        $reader = New-Object System.IO.StreamReader($stream)
        try {
            $content = $reader.ReadToEnd()
        }
        finally {
            $reader.Dispose()
        }
    }
    finally {
        $stream.Dispose()
    }

    $xml = New-Object System.Xml.XmlDocument
    $xml.PreserveWhitespace = $true
    $xml.LoadXml($content)
    return $xml
}

function Convert-DocxToMarkdown {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputPath,
        [Parameter(Mandatory = $true)]
        [string]$OutputPath
    )

    $zip = [System.IO.Compression.ZipFile]::OpenRead($InputPath)
    try {
        $xml = Read-ZipXml -Zip $zip -EntryPath 'word/document.xml'
    }
    finally {
        $zip.Dispose()
    }

    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $ns.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

    $body = $xml.SelectSingleNode('//w:body', $ns)
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("# $([System.IO.Path]::GetFileNameWithoutExtension($InputPath))")
    $lines.Add('')

    foreach ($child in $body.ChildNodes) {
        if ($child.LocalName -eq 'p') {
            $text = Get-InnerText -Node $child -Ns $ns
            if ($text) {
                $lines.Add($text)
                $lines.Add('')
            }
            continue
        }

        if ($child.LocalName -eq 'tbl') {
            $rows = @()
            foreach ($tr in $child.SelectNodes('./w:tr', $ns)) {
                $cells = @()
                foreach ($tc in $tr.SelectNodes('./w:tc', $ns)) {
                    $cellText = Get-InnerText -Node $tc -Ns $ns
                    $cells += (Escape-MarkdownCell $cellText)
                }
                while ($cells.Count -gt 0 -and [string]::IsNullOrWhiteSpace($cells[-1])) {
                    $cells = if ($cells.Count -eq 1) { @() } else { $cells[0..($cells.Count - 2)] }
                }
                if ($cells.Count -gt 0) {
                    $rows += ,@($cells)
                }
            }

            if ($rows.Count -gt 0) {
                $columnCount = ($rows | ForEach-Object { $_.Count } | Measure-Object -Maximum).Maximum
                $normalized = foreach ($row in $rows) {
                    $copy = @($row)
                    while ($copy.Count -lt $columnCount) {
                        $copy += ''
                    }
                    ,$copy
                }

                $header = $normalized[0]
                $lines.Add('| ' + ($header -join ' | ') + ' |')
                $lines.Add('| ' + ((@('---') * $columnCount) -join ' | ') + ' |')
                foreach ($row in $normalized | Select-Object -Skip 1) {
                    $lines.Add('| ' + ($row -join ' | ') + ' |')
                }
                $lines.Add('')
            }
        }
    }

    $content = ($lines -join "`r`n").TrimEnd() + "`r`n"
    [System.IO.File]::WriteAllText($OutputPath, $content, [System.Text.UTF8Encoding]::new($false))
}

function Get-ExcelColumnIndex {
    param([string]$CellRef)
    $letters = ($CellRef -replace '\d', '')
    $value = 0
    foreach ($char in $letters.ToCharArray()) {
        $value = ($value * 26) + ([int][char]::ToUpperInvariant($char) - [int][char]'A' + 1)
    }
    return $value
}

function Get-ExcelCellValue {
    param(
        [Parameter(Mandatory = $true)]
        [System.Xml.XmlNode]$Cell,
        [string[]]$SharedStrings
    )

    $cellType = $Cell.Attributes['t']?.Value
    $valueNode = $Cell.SelectSingleNode('./*[local-name()="v"]')
    $inlineNode = $Cell.SelectSingleNode('./*[local-name()="is"]/*[local-name()="t"]')

    if ($cellType -eq 's' -and $valueNode) {
        return $SharedStrings[[int]$valueNode.InnerText]
    }
    if ($cellType -eq 'inlineStr' -and $inlineNode) {
        return $inlineNode.InnerText
    }
    if ($inlineNode) {
        return $inlineNode.InnerText
    }
    if ($valueNode) {
        return $valueNode.InnerText
    }
    return ''
}

function Convert-XlsxToMarkdown {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InputPath,
        [Parameter(Mandatory = $true)]
        [string]$OutputPath
    )

    $zip = [System.IO.Compression.ZipFile]::OpenRead($InputPath)
    try {
        $sharedStrings = @()
        if ($zip.Entries.FullName -contains 'xl/sharedStrings.xml') {
            $sharedXml = Read-ZipXml -Zip $zip -EntryPath 'xl/sharedStrings.xml'
            foreach ($si in $sharedXml.SelectNodes('/*[local-name()="sst"]/*[local-name()="si"]')) {
                $textParts = @()
                foreach ($t in $si.SelectNodes('.//*[local-name()="t"]')) {
                    $textParts += [string]$t.InnerText
                }
                $sharedStrings += ($textParts -join '')
            }
        }

        $workbookXml = Read-ZipXml -Zip $zip -EntryPath 'xl/workbook.xml'
        $relsXml = Read-ZipXml -Zip $zip -EntryPath 'xl/_rels/workbook.xml.rels'

        $relationshipMap = @{}
        foreach ($rel in $relsXml.SelectNodes('/*[local-name()="Relationships"]/*[local-name()="Relationship"]')) {
            $relationshipMap[$rel.Attributes['Id'].Value] = $rel.Attributes['Target'].Value
        }

        $lines = New-Object System.Collections.Generic.List[string]
        $lines.Add("# $([System.IO.Path]::GetFileNameWithoutExtension($InputPath))")
        $lines.Add('')

        foreach ($sheet in $workbookXml.SelectNodes('/*[local-name()="workbook"]/*[local-name()="sheets"]/*[local-name()="sheet"]')) {
            $sheetName = $sheet.Attributes['name'].Value
            $rid = $sheet.Attributes['r:id'].Value
            $target = $relationshipMap[$rid]
            if (-not $target) {
                continue
            }
            if (-not $target.StartsWith('xl/')) {
                $target = 'xl/' + $target.TrimStart('/')
            }

            $sheetXml = Read-ZipXml -Zip $zip -EntryPath $target
            $rows = @()
            foreach ($row in $sheetXml.SelectNodes('/*[local-name()="worksheet"]/*[local-name()="sheetData"]/*[local-name()="row"]')) {
                $cells = @()
                $expectedIndex = 1
                foreach ($cell in $row.SelectNodes('./*[local-name()="c"]')) {
                    $ref = $cell.Attributes['r'].Value
                    $currentIndex = Get-ExcelColumnIndex $ref
                    while ($expectedIndex -lt $currentIndex) {
                        $cells += ''
                        $expectedIndex++
                    }
                    $cells += (Escape-MarkdownCell (Get-ExcelCellValue -Cell $cell -SharedStrings $sharedStrings))
                    $expectedIndex++
                }
                while ($cells.Count -gt 0 -and [string]::IsNullOrWhiteSpace($cells[-1])) {
                    $cells = if ($cells.Count -eq 1) { @() } else { $cells[0..($cells.Count - 2)] }
                }
                if ($cells.Count -gt 0) {
                    $rows += ,@($cells)
                }
            }

            $lines.Add("## $sheetName")
            $lines.Add('')

            if ($rows.Count -eq 0) {
                $lines.Add('_空白工作表_')
                $lines.Add('')
                continue
            }

            $columnCount = ($rows | ForEach-Object { $_.Count } | Measure-Object -Maximum).Maximum
            $normalized = foreach ($row in $rows) {
                $copy = @($row)
                while ($copy.Count -lt $columnCount) {
                    $copy += ''
                }
                ,$copy
            }

            $header = $normalized[0]
            $lines.Add('| ' + ($header -join ' | ') + ' |')
            $lines.Add('| ' + ((@('---') * $columnCount) -join ' | ') + ' |')
            foreach ($dataRow in $normalized | Select-Object -Skip 1) {
                $lines.Add('| ' + ($dataRow -join ' | ') + ' |')
            }
            $lines.Add('')
        }

        $content = ($lines -join "`r`n").TrimEnd() + "`r`n"
        [System.IO.File]::WriteAllText($OutputPath, $content, [System.Text.UTF8Encoding]::new($false))
    }
    finally {
        $zip.Dispose()
    }
}

[System.IO.Directory]::CreateDirectory($OutputDir) | Out-Null

foreach ($file in Get-ChildItem -LiteralPath $SourceDir -File | Sort-Object Name) {
    $outputName = (Get-SafeFileName $file.BaseName) + '.md'
    $outputPath = Join-Path $OutputDir $outputName
    switch ($file.Extension.ToLowerInvariant()) {
        '.docx' { Convert-DocxToMarkdown -InputPath $file.FullName -OutputPath $outputPath }
        '.xlsx' { Convert-XlsxToMarkdown -InputPath $file.FullName -OutputPath $outputPath }
        default { Write-Warning "Skipped unsupported file: $($file.Name)" }
    }
    Write-Output "Converted $($file.Name) -> $outputName"
}
