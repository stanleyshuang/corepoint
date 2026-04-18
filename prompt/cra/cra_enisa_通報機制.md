CRA 下的 **ENISA 通報機制**，核心就是：
**製造商在發現特定資安事件後，不再分別向多個歐盟國家單位重複通報，而是透過 ENISA 建置的單一平台一次通報。** 這個平台叫做 **CRA Single Reporting Platform, SRP**。([歐洲數位未來][1])

你可以把它理解成一個「**單一入口、分流給正確主管機關**」的制度。

## 1. 這個機制是什麼

依 CRA，當產品已在歐盟市場上架後，若製造商得知：

* **被主動利用中的漏洞**（actively exploited vulnerabilities）
* **對產品安全造成重大影響的嚴重事件**（severe incidents）

就必須依法通報。自 **2026 年 9 月 11 日** 起，這項通報義務開始適用，通報工具就是 ENISA 建立與管理的 **SRP**。([歐洲數位未來][1])

ENISA 的角色不是單純收件而已。它負責建立、營運、維護這個平台，並確保平台的安全與資訊保護措施。([歐洲網絡與資訊安全局][2])

## 2. 由誰通報

主要義務人是 **manufacturer（製造商）**。
如果製造商 **不在 EU 境內設立**，則通報路徑會以其 **authorized representative（授權代表）所在成員國** 的協調 CSIRT 為準。([歐洲網絡與資訊安全局][2])

也就是說，對非歐盟企業而言，實務上要先釐清：

* 在 EU 是否有授權代表
* 該授權代表設立在哪個成員國
* 該國指定的 **CSIRT coordinator** 是誰

## 3. 通報給誰

表面上看像是「通報 ENISA」，但法律設計其實是：

1. 製造商透過 **SRP** 送件
2. 平台把通報送到：

   * 製造商**主要設立地**所在成員國的 **CSIRT coordinator**
   * **ENISA**（除非有特別例外情形）
3. 最先收到的 CSIRT 再把資訊**無延遲地**分送給其他相關成員國的 CSIRTs。([歐洲數位未來][1])

所以 **ENISA 是單一平台與中央節點**，但 **第一線國家層級處理者仍是 CSIRT**。

## 4. 什麼情況要報

CRA SRP 強制通報的內容有兩大類：

### A. 被主動利用中的漏洞

不是一般尚未被利用的普通漏洞，而是 **已知正遭惡意行為者利用** 的漏洞。([歐洲網絡與資訊安全局][2])

### B. 嚴重事件

是指對產品的 **availability / authenticity / integrity / confidentiality** 造成重大影響的事件。([歐洲網絡與資訊安全局][2])

這一點很重要：
CRA 的事件通報重點是 **「影響產品數位安全的漏洞與事件」**，不是所有企業營運層面的 incident 都歸 CRA。

## 5. 通報時限

CRA 採 **多階段通報**：

* **24 小時內**：先送 **early warning**
* **72 小時內**：送正式的初步通知，提供一般資訊與初步評估
* **最終報告**：

  * 若是 **actively exploited vulnerability**：在 **矯正措施可用後 14 天內**
  * 若是 **severe incident**：在 **首次通知後 1 個月內** 提交([歐洲數位未來][1])

實務上可把它理解成：

* 先快報
* 再補完整初判
* 最後補 remediation / root cause / impact 收斂資訊

## 6. 為什麼要做成單一平台

SRP 的目的，就是讓製造商 **只報一次**，不要自己去判斷每個成員國該各別投遞給誰。ENISA 明確說明，這套設計是為了簡化 CRA 下製造商的法定通報義務。([歐洲網絡與資訊安全局][2])

對企業實務的意義是：

* 減少多國重複通報成本
* 讓跨境資訊同步更快
* 由歐盟 CSIRT 網路統一分發與協調
* 讓 market surveillance authorities 在必要時取得資訊並啟動執法或矯正關注([歐洲網絡與資訊安全局][2])

## 7. ENISA 還做什麼

除了平台本身，ENISA 也有幾個配套角色：

* 管理與維運 SRP
* 提供協助，尤其是對 SME 的 helpdesk 支援
* 製作趨勢報告
* 在修補完成後，將相關漏洞資訊揭露至 **European Vulnerability Database（EUVD）** 的相應流程中([歐洲網絡與資訊安全局][2])

## 8. 這和 NIS2 / EUVD 不是同一件事

這裡很容易混淆：

* **CRA SRP**：是 CRA 下，給製造商做 **漏洞 / 事件通報** 的平台
* **EUVD**：是 ENISA 建立的 **歐洲漏洞資料庫**
* **NIS2 通報**：是特定重要/關鍵實體對其重大 incident 的通報義務，法制邏輯不同

ENISA 也明確提醒，**SRP 與 EUVD 是不同工具**。([歐洲網絡與資訊安全局][3])

## 9. 還有自願通報

除了法定強制通報外，SRP 也規劃支援 **voluntary reporting**。
自然人或法人可自願通報：

* 漏洞
* 可能影響產品風險輪廓的 cyber threat
* 事件
* near miss([歐洲網絡與資訊安全局][2])

這代表平台不只是 compliance channel，也可能成為 EU 層級產品安全資訊流的一部分。

## 10. 對廠商的實務建議

如果你是做產品安全 / PSIRT / 法遵，建議把 CRA ENISA 通報機制拆成這幾個準備項目：

1. **界定產品是否落入 CRA 範圍**
2. **建立「actively exploited vulnerability」判定標準**
3. **建立 severe incident 分級準則**
4. **盤點 EU main establishment / authorized representative**
5. **指定 24h / 72h / final report 內部責任人**
6. **準備通報欄位模板**：影響產品、版本、 exploitation 狀態、 IOCs、 workaround、 patch ETA、 已採取措施
7. **讓 PSIRT、法務、PR、產品團隊有同一套 escalation 機制**

不然真正出事時，最容易卡住的不是技術分析，而是：
**誰有權認定要不要報、往哪個成員國 CSIRT 報、72 小時內能交出什麼程度的內容。**

## 11. 一句話總結

**CRA 的 ENISA 通報機制 = 製造商自 2026/09/11 起，針對「遭利用中的漏洞」與「影響產品安全的嚴重事件」，透過 ENISA 建置的單一通報平台 SRP，在 24h / 72h / 最終報告的時限內完成一次性通報，由平台同步到對應 CSIRT 與 ENISA，再由 CSIRT 向其他成員國分發。** ([歐洲數位未來][1])

摘要：
CRA 下 ENISA 的重點不是取代國家主管機關，而是提供 **single reporting platform**，讓製造商「一次送件、依法分流、跨境同步」。若你要，我下一則可以幫你整理成 **PSIRT 內部 SOP 版流程圖** 或 **QNAP/供應商適用的通報模板欄位清單**。

[1]: https://digital-strategy.ec.europa.eu/en/policies/cra-reporting "Cyber Resilience Act - Reporting obligations | Shaping Europe’s digital future"
[2]: https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp "Single Reporting Platform (SRP) | ENISA"
[3]: https://www.enisa.europa.eu/news/consult-the-european-vulnerability-database-to-enhance-your-digital-security?utm_source=chatgpt.com "Consult the European Vulnerability Database to enhance your ..."
