以下是依 **CRA（EU Cyber Resilience Act, Regulation (EU) 2024/2847）公開官方資訊**整理的重點，分成你要的兩部分：

## 一、弱點通報機制與規定

CRA 已於 **2024 年 12 月 10 日生效**。其中與通報有關的 **Article 14** 會自 **2026 年 9 月 11 日**開始適用；CRA 其餘核心要求則自 **2027 年 12 月 11 日**全面適用。這點是歐盟官方摘要頁直接說明的。([數位策略網站][1])

### 1) 誰有通報義務

製造商對其 **products with digital elements**（含硬體、軟體、獨立上市的元件）有義務通報兩類事項：

1. **actively exploited vulnerabilities**：已知正遭惡意利用的弱點
2. **severe incidents**：對產品安全性造成嚴重影響的事件。([數位策略網站][2])

### 2) 通報對象與平台

製造商不是分別向多國逐一通報，而是透過 **CRA Single Reporting Platform (SRP)** 一次申報。
該通報會送到製造商主要設立地所在成員國的 **指定 CSIRT coordinator**，並原則上同步提供給 **ENISA**。SRP 由 ENISA 建置、管理與維運。([數位策略網站][2])

### 3) 通報時限

CRA 採 **多階段通報**：

* **24 小時內 early warning**：自製造商「知悉」已遭利用弱點或嚴重事件起，須無不當延遲且最遲於 24 小時內提出初步警示。([數位策略網站][2])
* **72 小時內正式通知**：須無不當延遲且最遲於 72 小時內提出較完整通知，包含一般資訊、初步評估等。([數位策略網站][2])
* **最終報告**：

  * 對於 **actively exploited vulnerabilities**：在可用的 corrective measure（例如 patch）出現後，**最遲 14 天內**提交。([數位策略網站][2])
  * 對於 **severe incidents**：自初始通知起 **1 個月內**提交。([數位策略網站][2])

### 4) 可 voluntary reporting 的事項

除了強制通報外，ENISA 的 SRP 說明也提到，自然人或法人可自願通報：

* 產品中的弱點
* 可能改變產品風險輪廓的 cyber threats
* 影響產品安全的 incidents
* near misses。([歐洲網絡與信息安全局][3])

### 5) 與 CVD（協調式弱點揭露）的關係

若 CSIRT 是在 **coordinated vulnerability disclosure** 過程中得知某個已遭利用弱點，基於正當的資安理由，CSIRT 得在必要期間內延後透過 SRP 擴散該資訊，直到相關揭露方同意揭露。這表示 CRA 在強制通報之外，也考量到 CVD 過程中的保密與時機控制。([歐盟法律總匯][4])

### 6) 通報後的資訊流向

法規規定，在有 security update 或其他 corrective / mitigating measure 可用後，ENISA 會與製造商協調，將已公開的弱點加入歐洲弱點資料庫（European vulnerability database）。([歐盟法律總匯][4])

---

## 二、弱點處理與揭露規定

CRA 不只要求「通報」，更要求製造商建立整套 **vulnerability handling process**。這些要求主要落在 **Annex I, Part II（Vulnerability handling requirements）**。([歐盟法律總匯][4])

### 1) 識別並記錄弱點與元件

製造商必須：

* **identify and document vulnerabilities**
* **identify and document components** contained in the product
* 並可透過 **SBOM** 方式完成，且 SBOM 應採常用、可機器讀取格式，至少涵蓋 top-level dependencies。([歐盟法律總匯][4])

### 2) 無不當延遲地處置與修補

製造商必須依風險對弱點 **address and remediate vulnerabilities without delay**，包括提供 **security updates**；在技術可行時，安全更新應與功能更新分開提供。([歐盟法律總匯][4])

### 3) 定期測試與審查產品安全

製造商須對產品進行 **effective and regular tests and reviews**，確保持續檢視安全性。([歐盟法律總匯][4])

### 4) 修補後的公開揭露義務

一旦 security update 已提供，製造商原則上要 **share and publicly disclose information about fixed vulnerabilities**，內容至少包括：

* 弱點描述
* 可識別受影響產品的資訊
* 弱點影響
* 嚴重度
* 清楚且可取得的 remediation 資訊。([歐盟法律總匯][4])

但 CRA 也允許例外：若製造商認為立即公開會讓安全風險大於安全利益，可在有正當理由下，**延後公開 fixed vulnerability 資訊**，直到使用者有機會先套用 patch。([歐盟法律總匯][4])

### 5) 必須建立並執行 CVD policy

製造商必須 **put in place and enforce a policy on coordinated vulnerability disclosure**。法規前言並補充，這份政策應有結構化流程，讓外部個人或組織能直接或透過指定 CSIRT 回報弱點，並讓製造商能先診斷與修補，再決定對第三方或公眾揭露。法規也明確提到，bug bounty programme 可作為 CVD policy 的一部分。([歐盟法律總匯][4])

### 6) 必須提供弱點聯絡窗口

製造商必須採取措施，方便外界分享產品及其第三方元件的潛在弱點資訊，包括提供 **contact address**。且產品相關資訊中應標示：

* 單一聯絡窗口（single point of contact）
* 哪裡可以回報/接收弱點資訊
* 哪裡可找到製造商的 CVD policy。([歐盟法律總匯][4])

### 7) 支援期間內持續處理弱點

CRA 強調製造商應在 **support period** 內有效處理弱點。法規前言指出，該支援期間原則上 **不得少於 5 年**，除非產品可合理預期使用壽命短於 5 年；若產品使用壽命預期更長，支援期間也應更長。工業場域產品通常被認為使用年限較長。([歐盟法律總匯][4])

---

## 可直接摘成程序書的結論

若你是要做公司內部程序書，CRA 對「弱點通報與揭露」可濃縮成這幾句：

1. **有已遭利用弱點或嚴重事件時，要走 SRP 強制通報流程。**
   24 小時 early warning、72 小時正式通知、之後依類型交最終報告。([數位策略網站][2])

2. **平時就必須有完整 vulnerability handling process。**
   包含弱點識別、元件盤點/SBOM、修補、測試、security update 發布、公開 fixed vulnerability 資訊。([歐盟法律總匯][4])

3. **必須建立 CVD policy 與單一通報窗口。**
   讓研究人員、客戶、CSIRT 可以回報弱點，並讓公司能在適當揭露時機前先完成診斷與修補。([歐盟法律總匯][4])

4. **對工業電腦/工控產品尤其要注意長支援週期。**
   CRA 明示工業環境產品往往使用年限較長，因此弱點處理與 security support 不應只看短期版本維護。([歐盟法律總匯][4])

---

### Recap

我已依 CRA 官方公開資訊整理出兩大塊：

* **弱點通報機制**：通報對象、SRP 平台、24h/72h/14d/1 month 時限
* **弱點處理與揭露規定**：SBOM、修補、公開揭露、CVD policy、聯絡窗口、支援期間

接下來若你要，我可以直接幫你再整理成 **「PSIRT 程序書條文版」** 或 **「Vulnerability Disclosure Process 條列版」**。

[1]: https://digital-strategy.ec.europa.eu/en/policies/cra-summary "The Cyber Resilience Act - Summary of the legislative text | Shaping Europe’s digital future"
[2]: https://digital-strategy.ec.europa.eu/en/policies/cra-reporting "Cyber Resilience Act - Reporting obligations | Shaping Europe’s digital future"
[3]: https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp "Single Reporting Platform (SRP) | ENISA"
[4]: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32024R2847 "Regulation (EU) 2024/2847 of the European Parliament and of the Council of 23 October 2024 on horizontal cybersecurity requirements for products with digital elements and amending Regulations (EU) No 168/2013 and (EU) No 2019/1020 and Directive (EU) 2020/1828 (Cyber Resilience Act) (Text with EEA relevance)"
