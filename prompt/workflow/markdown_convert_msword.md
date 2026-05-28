# 文件生成計畫：弱點處理與揭露程序轉換為 MS Word 程序文件

## 1. 計畫目的

將來源政策或程序 Markdown 轉換為可受控發行、可審閱、可重複產製的 MS Word 程序文件。產出文件需沿用既有 Word 樣本的頁首、頁尾、段落樣式與版面語氣，並依參考文件整理表格形式、章節結構與雙語呈現方式。

本計畫可重複套用於後續版本或其他 Level 2 / QP 類程序文件；每次執行時僅需替換「輸入參數」中的檔案、版本、日期與輸出名稱。

## 2. 本次輸入參數

本計畫以專案根目錄 `corepoint/` 為路徑基準，檔案依用途分置於 `doc/`、`template/`、`build/`、`persona/` 與 `prompt/workflow/`。

| 項目 | 本次設定 | 可重複使用時需確認 |
|---|---|---|
| 工作目錄 | 專案根目錄 `corepoint/` | 是 |
| 來源 Markdown | `doc/L2-01_vulnerability-handling-and-disclosure-process.md` | 是 |
| Word 樣本 | `template/樣本.docx` | 是 |
| 表格參考文件 | `template/QP-30-01 事件處理程序 V1.0 0528.docx` | 是 |
| 比對基準文件 | `doc/QP-30-01 事件處理程序 V1.0.docx` | 若已存在，視為 golden baseline，不得覆蓋 |
| 流程圖圖片 | `template/vul_handle_n_disclose_flow.png` | 視來源是否有流程圖 |
| 產出文件 | `doc/QP-30-01 事件處理程序 V1.0.docx`；若已存在則依第 2.1 節改名 | 是 |
| 主要生成腳本 | `build/build_qp_docx.py` | 視實作方式調整 |
| Python virtualenv | `.venv/` | 執行腳本前建立或確認 |
| Python 套件 | `python-docx` | 應安裝於 `.venv/`，不得全域安裝 |
| 術語表 | `prompt/translation/glossary_psirt.json` | 是 |
| 英文黑名單 | `prompt/translation/blacklist_english.json` | 是 |
| 人工翻譯記憶庫 | `prompt/translation/translation_memory_l2_01.json` | 是 |
| 自動翻譯候選腳本 | `build/generate_translation_candidates.py` | 視缺翻譯時使用 |
| 翻譯候選審查腳本 | `build/review_translation_candidates.py` | 視缺翻譯時使用 |
| Persona 目錄 | `persona/` | 固定或依專案調整 |

### 2.1 輸出檔名衝突處理

若指定產出文件已存在，生成流程不得覆蓋既有檔案，應依下列規則產生新的輸出檔名：

1. 優先使用原檔名加日期後綴，格式為 `_YYYYMMDD`，例如 `doc/QP-30-01 事件處理程序 V1.0_20260528.docx`。
2. 若日期後綴檔名仍已存在，依序加上版號 `_v2`、`_v3`，例如 `doc/QP-30-01 事件處理程序 V1.0_20260528_v2.docx`。
3. 版號應從 `v2` 開始遞增，直到找到不存在的檔名為止。
4. dry-run 時應只顯示原始輸出路徑、實際將使用的輸出路徑與是否會寫檔，不得建立或覆蓋任何 DOCX。

### 2.2 當前檔案關聯

1. `doc/L2-01_vulnerability-handling-and-disclosure-process.md` 是本次 Word 程序文件的主要內容來源。
2. `doc/QP-30-01 事件處理程序 V1.0.docx` 是本次已命名的目標輸出文件。
3. `template/樣本.docx` 是新文件應沿用頁首、頁尾、section、樣式與版面語氣的 Word 樣本。
4. `template/QP-30-01 事件處理程序 V1.0 0528.docx` 位於 `template/`，本計畫將其視為表格與版面參考文件，不作為正式輸出路徑。
5. `template/vul_handle_n_disclose_flow.png` 是來源 Markdown 中 Mermaid 程序總覽對應的流程圖圖片。
6. `build/build_qp_docx.py` 是主要生成腳本；執行前應確認其路徑設定與本節所列檔案位置一致。
7. `persona/python_docx_build_engineer.md` 是 Python 執行環境與 DOCX 建置驗證之專責 persona。
8. `prompt/translation/glossary_psirt.json`、`prompt/translation/blacklist_english.json` 與 `prompt/translation/translation_memory_l2_01.json` 是英文品質控制來源，應納入版控並經人工審閱。
9. `persona/translation_quality_reviewer.md` 是自動翻譯候選稿進入正式 translation memory 前的品質審查角色。
10. `build/generate_translation_candidates.py` 僅能產生 draft candidate 至 `tmp/translation_candidates_l2_01.json`，不得直接修改正式 translation memory 或 DOCX。
11. `build/review_translation_candidates.py` 僅能產生本地審查結果至 `tmp/translation_review_l2_01.json`，不得自動核准入庫。

### 2.3 既有基準文件狀態

1. 若 `doc/QP-30-01 事件處理程序 V1.0.docx` 已存在，該檔不得被視為可覆蓋輸出，而應作為本次生成結果的比對基準。
2. 目前 `doc/QP-30-01 事件處理程序 V1.0.docx` 與 `template/QP-30-01 事件處理程序 V1.0 0528.docx` 內容雜湊相同；因此本次可將兩者視為同一份 golden baseline。
3. 新生成檔應使用安全改名後的輸出路徑，例如 `doc/QP-30-01 事件處理程序 V1.0_YYYYMMDD.docx`，再與 golden baseline 比對。
4. 比對結論應區分內容差異、翻譯差異、表格差異、圖片差異、頁首頁尾 / section 差異與腳本或環境問題。
5. golden baseline 與既有產出 DOCX 不得作為可信英文翻譯來源；若其中英文品質未經人工審核，僅可作為版面與結構比對參考。

## 3. 參與 Persona 與分工

### 3.1 Context Engineer

負責分析文件生成需求、保留限制條件、確認輸入與輸出、拆解所需角色，並將一次性 prompt 整理為可重複使用的計畫文件。

### 3.2 PSIRT Process Reviewer

負責檢查來源內容是否維持 IEI PSIRT Level 2 程序意圖，包含 ISO/IEC 29147、ISO/IEC 30111、CRA、協調式揭露、Jira 留痕、修補驗證與揭露治理等要求。

### 3.3 Bilingual Document Editor

負責依樣本文件形式進行中英雙語編排。原中文為控制文字，英文為逐行或逐段草稿翻譯；專有名詞如 PSIRT、CVE、CVSS、SBOM、HBOM、Jira、CRA、EOL/EOS、ODM/OEM、CERT/CSIRT、CISA KEV 應保留英文。

### 3.4 DOCX OpenXML Builder

負責以 Word 樣本為基礎建立新 DOCX，保留頁首、頁尾、section 設定與樣式，移除樣本文字、表格與附圖後，將來源 Markdown 內容、表格與流程圖寫入新文件。

### 3.5 Python DOCX Build Engineer

負責建立與維護 `.venv/`，確認 `python-docx` 等依賴只安裝於專案 virtualenv，執行 dry-run、正式生成、OpenXML package 驗證與基準文件差異摘要。若因依賴、網路或權限造成腳本無法執行，應明確標示為建置環境問題，不應誤判為文件內容問題。

### 3.6 Persona 導入與優化責任

本 workflow 執行時應導入下列 persona 並套用其檢查重點：

1. Context Engineer：確認來源起點、輸出邊界、golden baseline、驗收條件與錯誤處理是否明確。
2. Bilingual Document Editor：確認新增或異動中文內容均有可接受英文對照；若缺翻譯，不得產生看似完成的 DOCX。
3. DOCX OpenXML Builder：確認 Markdown heading、清單、表格、Mermaid 圖片、頁首頁尾與 section 轉換未失真。
4. Python DOCX Build Engineer：確認 `.venv`、dry-run、fail-fast、輸出檔名避覆蓋、DOCX package 驗證與 ignored artifact 狀態。
5. Translation Quality Reviewer：審查外部 LLM / API 產生之 draft English candidate，確認術語、法遵語意、blacklist、污染句、數字與責任角色未失真；審查狀態可為 `approved`、`needs_revision`、`blocked` 或 `legal_review_required`。

## 4. 文件轉換原則

1. 以 `template/樣本.docx` 作為新文件主體。
2. 複製樣本文件後，保留頁首、頁尾、section、頁面設定、樣式定義與既有版面語氣。
3. 清除樣本文件 body 中的既有文字、表格與附圖。
4. 先辨識樣本中常用段落樣式，再將來源 Markdown 的章節、本文、清單與表格對應到適當樣式。
5. 來源 Markdown 的標題階層應保留，但標題文字中的前置數字章節編號應於 DOCX 輸出時移除。轉換規則為 `## <n>. xxxx` 輸出為 `## xxxx`，`### <n.n> xxxx` 輸出為 `### xxxx`；例如 `## 1. 目的 Purpose` 應輸出為 `目的 Purpose`，`### 2.1 適用性與風險式加嚴要求 Applicability and Risk-based Enhancements` 應輸出為 `適用性與風險式加嚴要求 Applicability and Risk-based Enhancements`。此規則僅適用於 Markdown heading；若來源為未加 `#` 的本文編號清單，例如 `1. PSIRT 與 RD/DQV 應確認案件是否可重現...`，輸出至 MS Word 時必須保留 `1.`，不得削去清單編號。
6. 來源 Markdown 的 bullet 清單應於中文段落反映 bullet 與縮排；若來源為縮排 bullet，例如 `   - 受影響 product family、型號、版本、平台與 BOM variant`，中文輸出應保留對應縮排並顯示 bullet。其英文翻譯段落應同步相同縮排，但不得顯示 bullet。
7. 表格形式應參考 `template/QP-30-01 事件處理程序 V1.0 0528.docx`，但最終字型與段落樣式仍以 `template/樣本.docx` 為準。
8. 當來源 Markdown 出現流程圖區塊或程序總覽位置時，插入 `template/vul_handle_n_disclose_flow.png`。
9. 依 `template/樣本.docx` 的雙語形式呈現：中文後緊接英文翻譯。
10. 中文來源文字為主控內容，不因英文草稿翻譯而改寫政策含義。
11. 不新增來源文件未明確支持的公司政策、責任承諾或法遵判定。
12. 來源 Markdown 的文件控制區塊僅供追溯使用；轉換時應明確排除自 `# L2-01：弱點處理與揭露程序 Vulnerability Handling and Disclosure Process` 起，至 `## 1. 目的 Purpose` 前一行為止的所有內容。`## 1. 目的 Purpose` 本身必須保留，但輸出至正式 DOCX body 時應移除章節編號，起始段落為 `目的 Purpose`。
13. 若來源 Markdown 的 Mermaid 區塊已由流程圖圖片取代，不應額外新增基準文件不存在的「流程圖 / Flow Chart」標題；圖片應插入於程序總覽章節中，並維持基準文件的圖片數量與位置邏輯。
14. 英文段落不得輸出 `[Draft translation]` 佔位字樣。若無法取得合格翻譯，應使用既有樣本 / 基準文件中的 translation memory，或將該段列入人工審閱清單，不得把機械替換文字寫入正式 DOCX。
15. 英文段落的縮排、行距、段前段後、對齊與分行分頁設定，應比照其相對應中文段落；英文樣式可保留字型語系差異，但 paragraph formatting 不得與對應中文段落分岔。
16. 來源正式內容起點應以可容忍章節號有無的方式辨識，例如 `## 1. 目的 Purpose` 或 `## 目的 Purpose`；若找不到起點，流程必須 fail-fast，不得回退為轉換整份 Markdown。
17. 若來源 Mermaid 區塊內容變更，應先更新對應 PNG 圖片並同步紀錄 Mermaid 來源 hash；不得在來源流程已變更時沿用舊流程圖。
18. 若新增或修改中文內容導致找不到英文對照，流程應 fail-fast 並輸出待翻譯清單，不得產出缺英文段落的正式 DOCX。
19. 英文翻譯來源僅允許使用人工審核之 `prompt/translation/translation_memory_l2_01.json`、`prompt/translation/glossary_psirt.json` 與腳本內已審核固定字串；不得自既有產出 DOCX、模板 DOCX 或機器翻譯結果自動建立可信 translation memory。
20. 英文輸出必須通過 `prompt/translation/blacklist_english.json` 品質 gate；若命中污染句、錯譯、錯字或禁止詞，流程應 fail-fast 並輸出 blocked English report。
21. 可使用外部 LLM / API 產生 draft translation candidate，但候選稿只能輸出至 `tmp/translation_candidates_l2_01.json`；候選稿必須經 Translation Quality Reviewer 審查與人工確認後，才可手動納入 `prompt/translation/translation_memory_l2_01.json`。
22. API key 應由環境變數提供，例如 `OPENAI_API_KEY`；不得寫入 repo、prompt、translation memory、candidate 或 review 檔。

## 5. 執行流程

### 5.1 專案盤點

1. 以專案根目錄為基準，檢查 `doc/`、`template/`、`build/`、`persona/` 與 `prompt/workflow/` 下的來源文件、樣本文件、參考文件、圖片、persona 與生成腳本是否存在。
2. 確認 `prompt/workflow/markdown_convert_msword.md` 或相關執行 prompt 中的輸入參數與實際檔名一致。
3. 確認來源 Markdown 是否包含章節、表格、流程圖區塊與修訂紀錄。
4. 檢查 `build/build_qp_docx.py` 的路徑設定是否與第 2 節一致，避免來源、樣本、圖片或輸出路徑錯置。
5. 檢查 `.venv/` 是否存在；若不存在，使用 `python3 -m venv .venv` 建立。
6. 使用 `.venv/bin/python -m pip show python-docx` 確認套件已安裝。若未安裝，應安裝於 `.venv/`，不得使用系統全域 Python 環境。
7. 確認 `prompt/translation/` 下的 glossary、blacklist 與 translation memory JSON 均存在且可解析。
8. dry-run 階段即應檢查來源正式內容起點、Mermaid hash、translation memory 格式與 blacklist；若檢查失敗，不得進入正式生成。

### 5.2 樣本與參考文件分析

1. 讀取 `template/樣本.docx`，記錄頁首、頁尾、section、字型、段落樣式與常見章節編排。
2. 讀取表格參考文件，觀察表格欄位、框線、字體大小、對齊與程序文件常見表現形式。
3. 讀取 `doc/QP-30-01 事件處理程序 V1.0.docx` 作為 golden baseline，記錄其起始段落、段落數、表格數、圖片數、頁首頁尾數與主要關鍵字分布。
4. 判定來源 Markdown 中哪些內容應呈現為標題、本文、清單、表格、圖片或修訂紀錄。
5. 明確排除來源 Markdown 中自 `# L2-01：弱點處理與揭露程序 Vulnerability Handling and Disclosure Process` 起，至 `## 1. 目的 Purpose` 前一行為止的文件控制資訊；正式 DOCX body 應自移除章節編號後的 `目的 Purpose` 開始。

### 5.3 內容審閱與結構化

1. 由 PSIRT Process Reviewer 檢查來源內容是否保留弱點處理與揭露程序的核心意圖。
2. 將 Markdown 標題、清單、表格與流程圖位置轉換為文件結構。
3. 對章節層級與編號進行必要整理，但不得改變來源政策含義。
4. 對需要後續人工確認的 L3 作業細節、管理核准、法遵判定或翻譯品質加註風險。

### 5.4 雙語編輯

1. 依中文原文產生英文草稿翻譯。
2. 中文與英文應相鄰呈現，符合樣本文件中一行中文後接一行英文的閱讀形式。
3. 英文翻譯應維持程序文件語氣，常用 shall / should / may 等規範語彙。
4. 專有名詞、標準、法規、系統名稱與縮寫不得任意翻譯或改寫。
5. 優先沿用 `prompt/translation/translation_memory_l2_01.json` 中已人工審核之中英對照作為 translation memory，以降低同一中文句子在不同產物中翻譯不一致的風險。
6. 生成式翻譯應視為 draft，需由文件擁有者、法務或流程負責人審閱。
7. 不得將 `[Draft translation]`、半中文半英文機械替換句或明顯不可讀英文寫入正式 DOCX；此類段落應標記為待人工翻譯與審閱。
8. 每一個英文段落建立後，應同步其對應中文段落的 paragraph formatting，至少包含 left/right/first-line indent、line spacing、space before/after、alignment、keep lines together、keep with next、page break before 與 widow/orphan control。
9. 若人工審核之 translation memory 或腳本內已審核固定字串無法提供英文對照，應輸出 missing translations report 並中止生成。
10. 不得從未經審核之既有 DOCX 擷取英文作為 translation memory；若需新增翻譯，應先更新 `prompt/translation/translation_memory_l2_01.json`，並由文件擁有者或 bilingual editor 審閱。
11. 若英文命中 blacklist，例如 `Syria Protests`、`sexed Vulnerability`、`CBOM/Parte`、`CPT/CSIRT`、`CERTT/CSIRT`、`CCA qualification`、`Exposition Status`、`Express Status` 或 `EPI status`，應輸出 blocked English report 並中止生成。
12. 若需使用外部 LLM / API 加速補齊翻譯，應先執行 `build/generate_translation_candidates.py` 產生 draft candidates，再執行 `build/review_translation_candidates.py` 做本地品質審查；只有人工審核通過者可手動入庫。

### 5.4.1 自動翻譯候選流程

自動翻譯不得直接進入正式 DOCX，應依下列流程處理：

1. DOCX 生成因缺英文翻譯中止後，使用 `tmp/missing_translations.txt` 作為輸入。
2. 設定 `OPENAI_API_KEY`；如需指定模型，可設定 `OPENAI_TRANSLATION_MODEL`，預設由候選產生腳本指定。
3. 執行 dry-run：`.venv/bin/python build/generate_translation_candidates.py --dry-run`。
4. 執行候選產生：`.venv/bin/python build/generate_translation_candidates.py --limit <N>`；建議先小批次處理高風險章節。
5. 執行本地審查：`.venv/bin/python build/review_translation_candidates.py`。
6. 人工審閱 `tmp/translation_review_l2_01.json`，僅將 `approved` 且不需法務確認之翻譯手動加入 `prompt/translation/translation_memory_l2_01.json`。
7. `legal_review_required` 項目須由法務、法遵或流程負責人審閱後才可入庫。
8. `needs_revision` 與 `blocked` 項目不得入庫，需修訂或重譯。
9. `tmp/translation_candidates_l2_01.json` 與 `tmp/translation_review_l2_01.json` 為工作產物，不納入 Git。

### 5.5 DOCX 建置

1. 以 `template/樣本.docx` 複製建立目標文件。
2. 移除 body 內容，保留 header、footer、style、section 與 package 結構。
3. 寫入整理後的雙語內容。
4. 套用樣本文件中對應的標題、本文與英文段落樣式；Markdown heading 輸出前應移除前置數字章節編號，但不得影響本文、清單、表格或法規條號中的數字。
5. 英文段落可使用英文樣式以維持字型與語系呈現，但其縮排、行距、段前段後與分行分頁設定應由對應中文段落複製；表格儲存格中的英文段落亦同。
6. 寫入表格並參考指定 QP 參考文件的表格形式。
7. 在程序總覽或來源流程圖位置插入流程圖圖片。
8. 依第 2.1 節的輸出檔名衝突處理規則，儲存為指定輸出檔名或自動遞增後的安全輸出檔名。
9. Markdown 表格解析應支援 escaped pipe `\|`，避免技術字串造成欄位錯位。

### 5.6 驗證

1. 確認輸出 DOCX 檔案存在且可作為有效 ZIP / OpenXML package 開啟。
2. 確認頁首與頁尾仍沿用樣本設定。
3. 確認主要章節、表格、流程圖與修訂紀錄已寫入。
4. 確認中文與英文段落相鄰呈現。
5. 確認流程圖圖片已插入在來源程序總覽位置。
6. 抽查表格欄位與清單內容，確認未遺漏來源 Markdown 的關鍵程序要求。
7. 抽查英文段落與對應中文段落的 paragraph formatting 是否一致，至少包含縮排、行距、段前段後、對齊與分行分頁設定。
8. 與 golden baseline 比對下列指標：檔案雜湊、段落數、表格數、表格列數、表格儲存格數、圖片數、header/footer 數、起始段落、關鍵字分布與 target-only / generated-only 段落樣本。
9. 若比對發現新檔多出來源 Markdown 開頭 `# L2-01...` 至 `## 1. 目的 Purpose` 前一行之間的內容、`[Draft translation]`、額外流程圖標題或圖片位置差異，應先修正轉換規則再產生下一版。
10. 標記仍需人工審閱的事項：英文翻譯、Word 視覺細節、法遵用語、管理核准與版本資訊。

### 5.7 Dry-run 驗證

1. 使用 `.venv/bin/python build/build_qp_docx.py --dry-run` 執行 dry-run，確認來源 Markdown、Word 樣本、流程圖圖片、glossary、blacklist 與 translation memory 路徑均存在。
2. 若 `doc/QP-30-01 事件處理程序 V1.0.docx` 已存在，dry-run 預期應回報 `resolved_output` 為加上當日日期後綴或日期加版號後綴的檔名。
3. dry-run 應同時檢查來源正式內容起點、Mermaid hash、translation memory 格式與 blacklist。
4. dry-run 應回報 `write=false`，且不得新增或覆蓋任何 DOCX。

### 5.8 差異分析重點

每次產出安全改名後的 DOCX，均應與 golden baseline 比對並特別注意：

1. 確認 golden baseline 與表格參考文件是否仍為同一份內容；若兩者不同，應以文件擁有者指定者為準。
2. 比對新產物與 golden baseline 的檔案雜湊、段落數、表格數、圖片數、header/footer 數與起始段落。
3. 若新產物多出 Markdown 開頭 `# L2-01...` 至 `## 1. 目的 Purpose` 前一行之間的任何內容，代表文件控制區塊未被正確排除。
4. 若新產物出現 `[Draft translation]`、半中文半英文機械替換句或明顯不可讀英文，代表 translation memory 或人工翻譯流程未完成。
5. 若表格數、圖片數、header/footer 數一致，但段落數或文字內容差異大，應優先檢查 body 文字結構、翻譯與章節起點，而非頁首頁尾或圖片嵌入。

## 6. 驗收標準

產出可視為完成初版建置時，需符合下列條件：

- 產出文件為 `doc/QP-30-01 事件處理程序 V1.0.docx`。
- 若 `doc/QP-30-01 事件處理程序 V1.0.docx` 已存在，實際產出應安全改名，並以既有檔作為 golden baseline 進行差異分析。
- 文件以 `template/樣本.docx` 為基礎，頁首與頁尾未被移除。
- `doc/L2-01_vulnerability-handling-and-disclosure-process.md` 主要內容已轉入 Word 文件。
- 表格以 Word 表格呈現，而非純文字。
- 流程圖圖片已插入適當章節。
- 文件呈現中英雙語，中文原文保留為控制文字。
- DOCX body 應自 `目的 Purpose` 開始，不得額外輸出來源 Markdown 中 `# L2-01...` 至 `## 1. 目的 Purpose` 前一行之間的文件控制區塊，且所有 Markdown heading 應移除前置數字章節編號。
- 英文段落不得包含 `[Draft translation]` 或明顯機械替換文字。
- 英文段落之縮排、行距、段前段後、對齊與分行分頁設定應與相對應中文段落一致。
- 若來源起點、Mermaid hash、英文翻譯完整性或 blacklist 檢查失敗，生成流程應中止並回報原因。
- DOCX package 結構有效，可由 Word 或相容工具開啟。
- 若指定產出文件已存在，新產物應依 `_YYYYMMDD`、`_YYYYMMDD_v2`、`_YYYYMMDD_v3` 的順序自動改名，不得覆蓋既有檔案。

## 7. 已知限制與人工審閱事項

1. 自動化生成可保留樣式與內容結構，但 Word 排版細節仍需人工視覺審閱。
2. 英文翻譯若由本地規則或機器翻譯產生，僅能視為草稿，不應直接作為法遵或正式對外文件使用。
3. 表格樣式可參考指定 QP 參考文件，但若樣本與參考文件樣式衝突，應由文件擁有者決定最終樣式。
4. CRA、主管機關通報、CNA 能力規劃、ODM/OEM 權責與客戶通知義務涉及法務或管理判定，需另行審閱。
5. 若來源 Markdown 後續新增 Mermaid、圖片、表格或特殊格式，生成腳本需同步調整解析規則。
6. 新增中文內容若未同步提供英文翻譯，生成流程會中止並輸出待翻譯清單；此為避免缺英文段落的刻意設計。
7. 若英文 blacklist 命中，生成流程會中止並輸出 blocked English report；此為避免污染英文再次進入 DOCX 的刻意設計。
8. 外部 LLM / API 產生之翻譯候選可能仍有語意反轉、術語漂移或法遵風險；必須經 Translation Quality Reviewer 與人工審核後才可入庫。

## 8. 後續重複使用方式

下次產製同類文件時，依序更新：

1. 來源 Markdown 路徑。
2. Word 樣本路徑。
3. 表格參考文件路徑。
4. 流程圖或附圖路徑。
5. 輸出 DOCX 檔名、版本與日期。
6. 需要啟用的 persona。
7. 驗收標準與人工審閱清單。
8. 生成腳本中的路徑常數或命令列參數。

更新後，依本計畫第 5 節流程重新執行即可。
