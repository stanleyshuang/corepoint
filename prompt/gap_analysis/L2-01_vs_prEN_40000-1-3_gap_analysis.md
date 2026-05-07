# L2-01 vs prEN 40000-1-3 差距分析

## 來源文件

- `L2-01_vulnerability-handling-and-disclosure-process 1-2026-04-24_08-31-24.md`
- `prEN_40000-1-3-2025-2026-04-01_09-29-32.md`

## 整體判斷

`L2-01` 已具備弱點處理流程主幹，包含受理、ACK、驗證、修補、揭露、CRA 通報與 Jira 留痕。

若要對齊 `prEN 40000-1-3:2025`，仍需補強標準要求的可稽核能力，尤其是準備階段、可近用溝通、SBOM/HBOM、定期測試與審查、監控來源清單、發布資訊格式與 EUVD。

目前 `L2-01` 引用 ISO/IEC 29147、ISO/IEC 30111、CRA，但未明確宣告對應 `prEN 40000-1-3`。

## 主要差距

| prEN 要求 | L2 現況 | 差距 |
|---|---|---|
| PRE-1 內部弱點處理政策需含完整流程、角色、時程、測試/審查策略、上游/下游客戶映射，並監控流程有效性。 | L2 有流程、角色、時程、指標。 | 部分符合。缺定期測試/審查策略與上游依賴清單需以 SBOM 完整性檢查的明確要求。 |
| PRE-2 CVD 政策需公開、可近用，並包含 contact、ongoing communication、report contents、secure communication、scope、publication、recognition、embargo 參數。 | L2 有外部通道、時限、最小訊息內容與禁止過早揭露。 | 部分符合。缺公開 CVD policy 必備欄位與 embargo 估算/協議參數。 |
| PRE-3 / PRE-5 作業安全與安全通訊，包含 need-to-know、TLP/標記、secure channel、匿名通報、不因安全機制破壞可近用性。 | L2 有 Jira 權限、敏感資料、PGP。 | 部分符合。缺匿名通報、TLP/敏感度分類標準、可近用性與安全通訊並存的要求。 |
| PRE-6 產品識別需至少 manufacturer name、product name、硬體/軟體識別碼，且硬軟體分開提供。 | L2 要識別 product family、型號、版本、平台、BOM variant。 | 部分符合。缺產品識別欄位標準與硬體/軟體分離識別規則。 |
| PRE-7 SBOM 要求：所有軟體元件、producer/name/version、top-level dependency、可行時 transitive dependency、SPDX/CycloneDX、metadata、PURL/CPE/SWHID/hash。 | L2 僅說必要時對應 SBOM。 | 高差距。L2 未定義 SBOM 生成、格式、欄位、更新時機、完整性證據。 |
| PRE-8 硬體元件識別，需 hardware producer、component name、firmware version、component identifier 等。 | L2 僅提 BOM variant、第三方元件。 | 高差距。缺 HBOM/硬體安全相關元件清單與欄位。 |
| PRE-9 / RCP-6 / RCP-7 需風險式 security test and review plan，且依計畫執行；風險評估輸入至少每年檢視。 | L2 只有案件處理後檢討與稽核指標。 | 高差距。缺產品支援期間內的定期弱掃、測試、審查、年度風險重評要求。 |
| RCP-2 需監控內外部來源，最低包含 EUVD、通報、定期測試、定期審查，並監控第三方元件 EOS/usage。 | L2 有 VirusTotal、CISA KEV、GreyNoise 指標與第三方協調。 | 部分符合。缺 EUVD、監控來源清單、監控頻率、第三方元件 EOS/使用狀態監控。 |
| RLS-1 安全更新需免費提供，除 tailor-made product 與 business user 另有約定；需及時分發、安裝說明、完整性/真實性。 | L2 有安裝/驗證/回復說明、分開交付、雜湊/簽章。 | 部分符合。缺安全更新免費與 tailor-made 例外條款。 |
| RLS-2 fixed vulnerability 資訊需 human-readable，enhanced requirement 需 machine-readable，且建議 EUVD；公告需 release/update date。 | L2 有公告最小內容。 | 部分符合。缺 machine-readable advisory、EUVD 發布/同步、release date/update date。 |
| PRA-1 post-release actions 需 case maintenance 與 remediation monitoring。 | L2 有結案確認與 lessons learned。 | 部分符合。缺修補發布後的採用狀態、失敗率、回報、再發監控。 |

## 優先補強建議

1. 在 L2 文件的「適用標準」加入 `prEN 40000-1-3:2025`，並新增 prEN 條款對照表。
2. 新增「準備能力」章節：SBOM、HBOM、上游/下游 stakeholder mapping、定期 security test/review plan。
3. 補強 CVD 公開政策欄位：report contents、scope、recognition、secure communication、accessibility、embargo 參數。
4. 建立監控要求：EUVD、CVE/NVD、CISA KEV、供應商公告、OSS 維護/EOS、內部測試與審查結果。
5. 補上發布格式：human-readable advisory、machine-readable advisory、EUVD/CVE 同步、release date/update date。
6. 補上 post-release remediation monitoring，不只結案，也追蹤更新分發、客戶套用、修補失敗與再發問題。

## 最高風險缺口

最高風險缺口是 SBOM/HBOM、定期測試/審查、EUVD/元件監控與 machine-readable advisory。這些是 prEN 明確要求可提出證據的項目，單靠目前 Jira 案件流程不足以證明符合。
