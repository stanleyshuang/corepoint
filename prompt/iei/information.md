以下為依 **IEI 威強電工業電腦公開資訊** 所做的整理，目的是作為後續擬定 **Vulnerability Disclosure Process**、對齊 **ISO/IEC 29147** 與 **ISO/IEC 30111** 的基礎盤點。
我把「官方已明示」與「依公開資訊推估」分開寫，避免把推論當成事實。 ([IEI World][1])

---

## 1) 公司類型、所屬產業、產業鏈位置

### 公司類型

IEI 官方將自己定位為 **全球工業電腦（IPC）與 AIoT 解決方案供應商**，並明示提供 **ODM/OEM 服務**；產品涵蓋嵌入式系統、邊緣運算平台、平板/觸控電腦等。 ([IEI World][2])

### 所屬產業

依官網與年報，IEI 所屬核心產業可歸納為：

* **工業電腦 / 嵌入式運算產業**
* **AIoT / Edge AI**
* **網路通訊設備**
* **智慧醫療 / 醫療電腦**
* **工業自動化 / 智慧製造** ([IEI World][1])

### 產業鏈位置

從公開資訊看，IEI 不只是零件採購方，也不是純軟體商，而是位在 **中游偏系統整合端** 的角色：

1. 向上游採購 CPU、GPU、記憶體、儲存、主機板零組件、韌體/OS 生態資源。
2. 在中游完成 **產品規劃、設計、驗證、製造管理、供應商管理、售後支援**。
3. 向下游提供 **標準產品 + ODM/OEM 客製化 + 產業解決方案** 給品牌商、系統整合商、醫療/工控客戶。
   另外，IEI 年報明示 IPC 產業具少量多樣、客製化特性，且採 **MTO（Make to Order）接單生產模式**。 

---

## 2) 產品種類、描述、型號規則

### 產品大類

IEI 官網主選單與年報可整理出下列主要產品群：

* **AIoT & Edge Computing**
* **網路通訊**
* **嵌入式電腦**
* **嵌入式系統**
* **觸控電腦與顯示器**
* **Power Supply**
* **Peripherals**
* 另在部分頁面可見 **醫療電腦**、**Advanced Video Solution**、**Software / ePaper** 等延伸分類。 ([IEI World][3])

### 產品描述

官網首頁與產品頁顯示，IEI 主要提供：

* **工業主機板 / SBC**：如 IMBA、WAFER、HYPER、KINO 等系列。 ([IEI World][4])
* **無風扇工業電腦 / Box PC / Edge AI 系統**：如 TANK、TANGO、FLEX、HTB 等。 ([IEI World][5])
* **網通設備 / Firewall / Network Appliance**：如 PUZZLE 系列。 ([IEI World][1])
* **Panel PC / 工業顯示器**：如 PPC、PPC2、DM2 等系列。 ([IEI World][6])
* **醫療 AI Box PC / 醫療平板 / 醫療主機板**：如 HTB、POCr、Thin Mini-ITX 醫療應用。 ([IEI World][1])

### 型號規則（依公開產品頁推估）

IEI 官網沒有看到一份官方「命名規則總表」，但從大量型號可推估有高度一致的 family-based 命名邏輯：

* **IMBA-***：多為 **ATX / industrial motherboard** 類主機板；後綴常帶平台或晶片組，例如 `IMBA-R680`、`IMBA-ADL-H610`、`IMBA-AM5`、`IMBA-Q370`。
  這代表 **家族名 + CPU/Chipset/平台代號**。 ([IEI World][4])

* **WAFER-***：多為 **3.5" SBC**；後綴常帶 Intel / Rockchip 平台，如 `WAFER-ADL-N`、`WAFER-RK3588`。 ([IEI World][7])

* **HYPER-***：多為 **PICO-ITX / 小型 SBC**；後綴常帶 SoC 平台，如 `HYPER-RK39`、`HYPER-RK3566`。 ([IEI World][8])

* **KINO-***：多為 **Mini-ITX / Thin Mini-ITX 主機板**；後綴帶平台代號，如 `KINO-TGL-U`。 ([IEI World][9])

* **TANK-***：多為 **高效能無風扇嵌入式電腦 / Edge AI 系統**；如 `TANK-XM811`、`TANK-XM813`、`TANK-8700-MPHX`。其中後綴常反映平台或 CPU 代系。 ([IEI World][10])

* **PUZZLE-***：多為 **網路通訊設備 / firewall appliance / network appliance**；如 `PUZZLE-1100`、`PUZZLE-IN004`、`PUZZLE-A001`。後綴常映射網通平台或 CPU 供應商路線。 ([IEI World][1])

* **PPC / PPC2 / DM2 / HTB / TANGO / FLEX**：分別對應 panel PC、monitor、medical box pc、mini pc、模組化/機架式系統等產品族。 ([IEI World][6])

**結論**：IEI 的型號規則看起來是典型 IPC 廠商做法：
**產品家族代號 + 平台/晶片組/尺寸/用途代號 + 區域/版本尾碼**。
這對 PSIRT 很重要，因為後續 VDP 應以 **product family / platform / SKU / BOM variant** 做影響評估，而不是只靠單一商業品名。上述命名規則屬依公開頁面推估，非官網明文命名政策。 ([IEI World][8])

---

## 3) 上游供應商、可能的上游供應商

### 官網可直接辨識的上游/技術夥伴

從 IEI 產品頁與方案頁，可直接看到下列平台或技術來源：

* **Intel**：大量主機板、Box PC、網通產品以 Intel Core / Xeon / chipset 為基礎。 ([IEI World][4])
* **AMD**：主機板與網通設備使用 AMD Ryzen / EPYC 平台。 ([IEI World][11])
* **NVIDIA**：醫療/AI Box PC 支援 NVIDIA GPU acceleration card。 ([IEI World][1])
* **Rockchip**：ARM SBC/嵌入式板卡使用 RK3566、RK3588、RK3399。 ([IEI World][12])
* **Microsoft**：在 IEI 產品搜尋結果可見「IEI 是 Intel, AMD 和 Microsoft 的合作夥伴」描述。 ([IEI World][13])
* **Google Cloud**：IEI AI Ready Solution 頁面明示與 Google Cloud 合作。 ([IEI World][14])
* **QNAP（集團內成員）**：AI Ready Solution 頁面明示 IEI 與集團成員 QNAP 協作，用於 storage、netcom、smart video 方案。 ([IEI World][14])
* **Coral**：官方新聞明示與 Coral 合作擴展 edge AI business。 ([IEI World][15])
* **十銓 Team Group**：官方新聞顯示 MCS-DB001 內部搭載十銓寬溫儲存元件。 ([IEI World][16])

### 可能的上游供應商（依產品結構推估）

若以 IPC/BMC/firmware/OS 供應鏈常態推估，IEI 可能還會依產品別依賴：

* BIOS / UEFI / EC / BMC 相關韌體供應商
* DRAM / SSD / eMMC / NIC / Wi-Fi 模組供應商
* ODM/OEM 專案中的外包設計、代工與測試資源
* Linux / Android / Windows 生態元件供應鏈
  這部分官網未逐一列名，因此應標示為 **可能供應商群，不宜在程序文件中寫成既定事實**。較適合在內部 VDP/PSIRT 流程中設為 **第三方元件與供應商協調節點**。 

---

## 4) 客戶、可能之客戶

### 官網可直接辨識的客戶/合作對象

IEI 官網成功案例與新聞可直接看到：

* **LPIXEL Inc.**：選用 HTB-210-Q470 做 AI-powered endoscopic imaging diagnosis。 ([IEI World][17])
* **敦揚醫學科技**：與 IEI 合作打造內視鏡完整解決方案。 ([IEI World][18])
* **全球礦業解決方案供應商**：採用 IEI rugged panel PC 進行礦場數位轉型，但新聞未明示公司名。 ([IEI World][19])
* **AMR 管理系統客戶**：導入 iVEC 邊緣虛擬化平台，名稱未公開。 ([IEI World][20])

### 可能之客戶類型

依 IEI 官網解決方案與應用領域，可能客群包括：

* **工廠自動化 / 智慧製造客戶**
* **醫療器材商、醫療品牌商、醫院系統整合商**
* **網通/資安設備商、SMB firewall appliance 客戶**
* **智慧交通、智慧建築、智慧零售整合商**
* **AMR / 機器人 / 邊緣 AI 導入客戶**
* **ODM/OEM 品牌客戶** ([IEI World][1])

對 VDP 而言，這表示 IEI 不是單純 B2C，而是 **B2B/B2B2B 型態**；弱點通報後常需考慮：

1. 標準品直接客戶；
2. ODM/OEM 品牌客戶；
3. 系統整合商；
4. 終端場域使用者。
   這一點與 ISO/IEC 29147 的「協調揭露、利害關係人通知」很吻合。此段最後一句屬依公開商業模式所做之合理推論。 ([IEI World][3])

---

## 5) 組織、部門、PM / RD / DQV 與產線分工

### 官網/年報可直接看到的主要部門

112 年年報「各主要部門所營業務」顯示：

* **網通暨邊際運算事業中心**：
  負責市場趨勢研究、符合市場/客戶需求的產品規劃、產品週期或專案進度管理、跨部門協調、行銷企劃、通路開發、客戶管理、業務訂單流程。 
* **醫療事業中心**：年報顯示為主要組織之一。 
* **研發中心**：
  負責產品開發、設計、驗證；新技術/新製程開發改良；售後問題技術支援。 
* **運籌中心 / 運籌管理處**：
  負責原物料/成品庫存統籌、產銷協調、外包廠商遴選與委外管理、供應商管理、詢比議價、採購與催料。 
* **製造處**：
  負責產品製造、生產管理、倉庫與物流進出貨。 
* **品質處**：
  負責原材料/成品品質規範管理與檢驗、售後客訴與維修服務、品質管理系統建立維護。 
* **資訊服務處**：
  負責資訊系統規劃、建構、開發與 IT 維運。 

### PM 角色（依年報與招募資訊整合）

IEI 公開資訊雖未把 PM 職掌獨立成正式章節，但從年報與招募可清楚看出 PM/產品管理的核心角色：

* 市場趨勢研究
* 客戶需求轉產品規格
* 產品 roadmap / 產品週期管理
* 專案進度管理
* RD、生產、業務、法規等跨部門協調
* 針對 CRA 等法規把外部需求轉內部專案
  這些內容與一般 IPC 產品經理 / 專案經理職能一致。 

### RD 角色

官方年報與招募資訊明示 RD / 研發中心負責：

* 產品開發、設計、驗證
* 新技術、新製程開發與改良
* BSP / firmware / hardware / virtualization 等開發
* 售後技術支援
  104 徵才頁更指出研發中心專注 **X86 & ARM 主機板、Server、網通、ODM 專案設計**。 

### DQV 角色（依公開職缺語意推估）

我沒有在 IEI 官網找到正式「DQV 部門說明」，但從公開職缺與品質/測試相關描述可合理推估，IEI 的 **DQV / 設計驗證** 功能大致散落在：

* 研發中心內的設計驗證
* 硬體測試工程師
* EMC / 安規工程師
* 品質處
  公開職缺顯示其工作內容涉及：
* 系統研發專案之產品測試
* 測試報告分析
* 問題排除
* EMC 設計/驗證/除錯
* 認證委外與法規符合追蹤
  因此，若要在程序書中定義 DQV，較合理的寫法是：
  **DQV 負責設計驗證、功能/相容性/法規與安規驗證、缺陷重現與驗證關卡管理，並與 RD/品質/PM 協作完成 release gating。**
  這是依公開資訊推估，不是官網明載名稱。 ([104人力銀行][21])

### 產線/製造分工

依年報，量產相關責任可切成：

* **運籌中心**：供應商、採購、物料、外包管理、產銷協調。 
* **製造處**：生產執行、倉庫、物流。 
* **品質處**：IQC/OQC/品質系統/客訴維修。 
* **研發中心**：設計與驗證、技術支援。 
* **事業中心 / PM**：產品規劃、客戶需求、專案協調。 

這種分工很適合在 ISO/IEC 30111 程序中做 RACI：

* PM：owner of product impact & customer coordination
* RD：owner of technical analysis & fix
* DQV/QA：owner of validation & release evidence
* SCM/MFG：owner of BOM / supplier / production execution
* PSIRT：owner of intake / triage / disclosure governance

---

## 6) 現有 Vulnerability Disclosure Process 描述

### 已公開的制度元件

IEI 官網已公開下列與漏洞揭露有關的機制：

1. **產品資安通報入口**
2. **安全弱點獎勵計畫**
3. **弱點披露政策**
4. **PSIRT 啟動公告** ([IEI World][22])

### 回報方式

IEI 安全弱點獎勵計畫頁面明示：

* 研究人員應使用 **PGP 公開金鑰** 加密後寄至 **[security@ieiworld.com](mailto:security@ieiworld.com)**
* IEI PSIRT 會聯絡研究員確認提交資料。 ([IEI World][23])

### 已公開的時程

IEI 官網目前已公開的處理節點包括：

* 系統自動回覆技術申請單號
* **7 天內啟動分析**
* **啟動後 14 天內確認是否受理**
* 若確認為弱點，依嚴重性儘速修補
* **整體流程至少 90 天**
* 若需補件，以補件完成日重新起算。 ([IEI World][23])

### 弱點評估與分類

IEI 明示採 **CVSS v3.x** 作為主要評估基準，並結合：

* 影響範圍
* 可利用度
* 修補複雜度與替代方案
  風險等級分為 Low / Medium / High / Critical。 ([IEI World][24])

### 揭露原則

IEI 的披露政策目前核心原則是：

* 原則上在 **修補程式或有效緩解措施可用後** 才揭露
* 若弱點已廣泛知悉或疑似遭利用，可能提前公告並提供暫時建議
* Critical/High 原則上在 patch/mitigation 就緒後揭露
* Medium/Low 一般在完整解決方案就緒後，且可能併入整合式公告。 ([IEI World][24])

### 修補時程

目前官網公開之修補預估為：

* **Critical / High：30–90 天**
* **Medium：3–6 個月或下一重大版本**
* **Low：依產品生命週期排程，可延後或併入例行維護** ([IEI World][24])

### 特殊情況

官網另明示：

* **EOL/EOS 產品**：僅能提供 best effort 建議或風險指引
* **低風險但高成本修補**：可先提供暫時性保護措施
* **OEM/ODM 客製專案**：若客戶選擇不實施修補，IEI 提供風險告知並尊重客戶決定。 ([IEI World][24])

### 與 ISO/IEC 29147 / 30111 的差距觀察

從公開頁面看，IEI 已具備 29147/30111 的基本骨架：

* 有聯絡窗口
* 有安全研究員提交方式
* 有初步 SLA
* 有風險分級
* 有揭露原則
* 有 patch policy / EOL / OEM-ODM 特例
  但若要更貼近標準，仍建議在正式程序書補強：
* 明確的 **intake → triage → remediation → disclosure → closure** 流程圖
* 明確 RACI（PSIRT / PM / RD / DQV / QA / Legal / Sales / ODM account）
* 第三方元件與上游供應商協調流程
* CVE/CNA、公告模板、客戶預先通知條件
* 內外部時程分層：acknowledgement、acceptance、fix target、advisory release
* OEM/ODM 與品牌客戶之 coordinated disclosure 規則
  這一段是依標準要求對現況的分析，不是 IEI 官網原文。支撐現況描述的事實依據如下。 ([IEI World][23])

---

## 7) 可直接帶入程序書的 IEI 輪廓結論

若你要把這份盤點轉成程序書前言或適用範圍，可這樣定義 IEI：

> IEI 為工業電腦（IPC）與 AIoT 解決方案供應商，採標準品與 ODM/OEM 並行模式，產品涵蓋嵌入式主機板、嵌入式系統、網通設備、工業顯示與觸控電腦、醫療電腦與邊緣 AI 平台，應用於智慧製造、網路通訊、醫療、交通、零售與建築等場域。其供應鏈涉及 CPU/GPU/SoC、儲存、OS 與第三方軟體/韌體元件，漏洞處理需涵蓋標準產品、客製產品、上游元件供應商及下游客戶/整合商之協調揭露。
> 這段是根據公開資訊整理後的綜合表述。 ([IEI World][3])

---

## 摘要

* IEI 公開定位明確：**IPC + AIoT + ODM/OEM**，且採 **MTO 接單生產**。
* 部門分工可從年報重建出 **事業中心 / 研發中心 / 運籌 / 製造 / 品質** 的責任鏈。
* 現行官網已具備 **PSIRT、VDP、Bounty、CVSS 分級、初步 SLA、披露與修補政策**。
* 缺口主要不在「沒有制度」，而在 **需要把公開政策再內化成標準化流程、RACI、第三方協調與公告機制**。

下一步若你要，我可以直接把這份盤點轉成一版 **IEI 專用 Vulnerability Disclosure Process 程序書架構**，並對齊 **ISO/IEC 29147 + ISO/IEC 30111**。

[1]: https://www.ieiworld.com/tw/ "IEI 威強電 工業電腦 | AIoT, 嵌入式系統 - 觸控電腦 – 無風扇工業電腦 - 工業自動化 – 網路通訊設備"
[2]: https://www.ieiworld.com/tw/about/index_cat.php?cat=1&utm_source=chatgpt.com "威強電工業電腦股份有限公司簡介"
[3]: https://www.ieiworld.com/tw/news/con_show.php?cid=1403&op=showone "IEI 2025 年度回顧：持續擴展Edge AI的核心能力"
[4]: https://www.ieiworld.com/tw/product/model.php?II=887&utm_source=chatgpt.com "IEI IMBA-R680 ATX Motherboard | Supports 12th/13th Gen ..."
[5]: https://www.ieiworld.com/tw/product/model.php?II=1099&utm_source=chatgpt.com "TANK-XM813"
[6]: https://www.ieiworld.com/tw/product/items_by_cat_intro.php?CA=5&utm_source=chatgpt.com "觸控電腦與顯示器:: Product overview"
[7]: https://www.ieiworld.com/tw/product/_pdf/?utm_source=chatgpt.com "IEI E-catalog"
[8]: https://www.ieiworld.com/tw/product/model.php?II=610&utm_source=chatgpt.com "IEI HYPER-RK39 Pico-ITX Single Board Computer ..."
[9]: https://www.ieiworld.com/tw/product/model.php?II=875&utm_source=chatgpt.com "KINO-TGL-U Thin Mini-ITX motherboard with the 11th ..."
[10]: https://www.ieiworld.com/tw/product/model.php?II=886&utm_source=chatgpt.com "IEI TANK-XM811 High-Performance 12th Generation Intel ..."
[11]: https://www.ieiworld.com/tw/product/model.php?II=1038&utm_source=chatgpt.com "IMBA-AM5"
[12]: https://www.ieiworld.com/tw/product/model.php?II=973&utm_source=chatgpt.com "HYPER-RK3566"
[13]: https://www.ieiworld.com/tw/product/model.php?II=1118&utm_source=chatgpt.com "TANK-8700-MPHX"
[14]: https://www.ieiworld.com/tw/support/con_show.php?cid=87&op=showone "AI Ready Solution | IEI"
[15]: https://www.ieiworld.com/tw/news/con_show.php?cid=1255&utm_source=chatgpt.com "IEI Launches New Powerful AI Accelerator PCIe Cards with ..."
[16]: https://www.ieiworld.com/tw/news/con_show.php?cid=1405&op=showone&utm_source=chatgpt.com "雙強聯手演繹AI 邊緣運算與高資安防護的完美整合"
[17]: https://www.ieiworld.com/tw/news/con_show.php?cid=1384&op=showone&utm_source=chatgpt.com "AI-Powered Endoscopic Imaging Diagnosis Case Study"
[18]: https://www.ieiworld.com/tw/news/con_show.php?cid=1392&op=showone "從內視鏡到AI運算，威強電布局智慧醫療全新藍圖"
[19]: https://www.ieiworld.com/en/news/con_show.php?cid=1395&utm_source=chatgpt.com "Transforming Open-Pit Mining with IEI Rugged Panel PC"
[20]: https://www.ieiworld.com/tw/news/con_show.php?cid=1402&op=showone&utm_source=chatgpt.com "威強電緊湊型邊緣伺服器：虛擬化平台，降低AMR 管理系統總 ..."
[21]: https://events.104.com.tw/ieiworld/20250820172138/ "〖加入威強電〗招募工程師/產品經理/國內外業務｜-104人力銀行"
[22]: https://www.ieiworld.com/tw/finance/con_show.php?cid=3&op=showone "公司年報 :: 財務資訊 :: IEISolution :: IEI"
[23]: https://www.ieiworld.com/tw/support/con_show.php?cid=102 "安全弱點獎勵計畫"
[24]: https://www.ieiworld.com/tw/support/con_show.php?cid=107 "漏洞披露政策"

---
若以 **IEI 這種工業電腦 / AIoT / ODM-OEM 製造商** 的脈絡來看，**PSIRT 最佳實踐** 不是只有「有一個通報信箱」而已，而是要把 **外部揭露（ISO/IEC 29147）** 與 **內部處理（ISO/IEC 30111）** 串成一條可執行的治理鏈。NIST 也明確把 ISO/IEC 29147 與 ISO/IEC 30111 視為漏洞揭露與處理的基礎；FIRST 的 PSIRT Services Framework 則提供了實務上常用的服務面向與成熟度視角。([NIST CSRC][1])

## 一句話先講結論

對 IEI 這類公司，PSIRT 最佳實踐可以濃縮成這 8 件事：
**有清楚入口、可重現的分流機制、明確 owner、供應鏈協調能力、風險分級、修補驗證、分層通知、可持續量測。** 這些方向與 FIRST PSIRT Services Framework 對 PSIRT 服務與利害關係人管理的描述一致，也符合 CISA 對 VDP 的基本精神。([first.org][2])

---

## 1) 最佳實踐的核心框架

### A. 外部要有正式 Vulnerability Disclosure Policy / Report Channel

至少要公開：

* 哪些產品/服務在受理範圍
* 如何回報
* 允許/禁止的測試行為
* 研究人員期望的回覆節點
* 加密通報方式
* 法律善意條款或 safe harbor 原則
  這是 ISO/IEC 29147 的核心精神，也是 CISA 推動 VDP 時最強調的內容。Microsoft 的 CVD 與 CISA 的 VDP 平台都屬這種典型做法。([ISO][3])

### B. 內部要有完整 Vulnerability Handling Process

收到通報後，不能只靠 email 往返，而要有固定流程：

1. intake
2. triage
3. validation / reproduction
4. severity assessment
5. remediation planning
6. fix development
7. verification
8. advisory / disclosure
9. closure and lessons learned
   這正是 ISO/IEC 30111 的重點，也是 Siemens、Microsoft 這類成熟 PSIRT 的共通模式。([NIST CSRC][1])

### C. 要把利害關係人先定義清楚

FIRST PSIRT maturity 文件特別強調，PSIRT 成熟化的起點是先定義 stakeholder。對 IEI 來說，至少包括：

* 外部研究員
* 客戶 / ODM-OEM 客戶
* PM
* RD
* DQV / QA
* 法務 / PR / 業務
* 上游元件供應商
* 必要時的 CERT / CNA / 主管機關
  若 stakeholder 沒定義清楚，流程通常會卡在「誰決定要不要收案、誰負責修、誰負責發公告」。([first.org][4])

---

## 2) 成熟 PSIRT 的實務範例長什麼樣

### 範例 1：Cisco 型

Cisco 的公開做法很典型：有正式 Security Vulnerability Policy、PSIRT 團隊、固定 advisory 機制，並且把漏洞揭露與 customer communication 視為持續性流程，而不是一次性回覆。這種模式很適合產品線多、全球客戶多、版本分支多的公司。([Cisco][5])

你可以從 Cisco 型學到三件事：

* **政策公開且穩定**
* **漏洞公告格式標準化**
* **PSIRT 是常設功能，不是臨時專案**
  這對 IEI 特別重要，因為 IPC 產品常有多 SKU、多平台、多生命周期並行。([Cisco][5])

### 範例 2：Siemens ProductCERT 型

Siemens 的流程更貼近 **OT / industrial** 場景。官方明示其 ProductCERT 會與開發團隊協作處理漏洞，必要時也會與國家 CERT 或政府 CERT 協調，並對已驗證的漏洞發布 Security Advisories。這很符合工業電腦廠商的需求，因為工控/OT 場景常牽涉：

* 現場不能立即停機
* 修補要考慮 safety / operation impact
* 需要 patch、upgrade、compensating control 並行
  對 IEI 而言，**Siemens ProductCERT 是最值得參考的產業型範例之一**。([Siemens][6])

### 範例 3：Microsoft MSRC 型

Microsoft 的重點在於：

* 明確 researcher portal
* CVD 原則
* 統一 update guide / release communication
* 對研究員與客戶提供可追蹤的資訊介面
  這種模式很適合想把流程數位化、平台化的企業。若 IEI 後續希望把安全通報、ticket、狀態追蹤、公告生成串進 Jira / portal，MSRC 是很好的參考對象。([Microsoft 安全響應中心][7])

---

## 3) 對 IEI 最有用的最佳實踐版本

你前面整理到 IEI 是 **中游偏系統整合端**，而且有 **ODM/OEM + MTO + 多產品家族 + 上游平台依賴**。因此，IEI 的 PSIRT 最佳實踐不應完全照抄純軟體公司，而應該是 **industrial product vendor / OEM-aware PSIRT**。這代表流程至少要有下面幾個特徵。先前你整理的 IEI 業務型態與供應鏈位置，也正好支持這種設計方向。([first.org][2])

### 3.1 產品導向，而不是單純漏洞導向

PSIRT 必須能回答的不只是「有沒有漏洞」，而是：

* 影響哪些 product family
* 影響哪些 platform / chipset / BOM variant
* 影響哪些 firmware / BIOS / driver / software app
* 標準品與 ODM 客製版是否同樣受影響
  這點對 IPC 廠尤其關鍵，因為同一顆 CPU 或同一個 BIOS issue，可能只影響特定板型、特定 BIOS branch、特定客製功能。這是 30111 在產品環境下真正困難的地方。([NIST CSRC][1])

### 3.2 必須有「第三方元件 / 供應商協調」分支

對 IEI 這類公司，弱點來源常見是：

* CPU / chipset / GPU
* BIOS / UEFI / firmware
* 第三方 library
* Linux / Windows / Android 元件
* Wi-Fi / BT / NIC module
  所以最佳實踐一定要把 case 分成：
* **IEI 自研缺陷**
* **第三方元件缺陷**
* **客製專案特有缺陷**
* **多方共同責任缺陷**
  Siemens 與 CVD 的實務都反映出這種協調需求；如果沒有這一層，流程只會停在「等供應商回覆」。([Siemens][6])

### 3.3 必須設計 OEM/ODM 客戶通知規則

對 B2B/ODM 型製造商，最佳實踐不是直接公開就結束，而是要有：

* 品牌客戶預先通知條件
* NDA 下的 advance notification
* 客戶是否自行發布公告
* IEI 是否保留母公告 / 子公告 / joint advisory 的權利
* 客戶若選擇不修補時的風險告知機制
  這在純 B2C 軟體商比較少見，但對 IPC / 醫療 / 工控 OEM 很常見。Siemens 對 partner CERT 與 advance coordination 的做法，很值得借鏡。([Siemens][6])

### 3.4 修補不只 patch，還要有 mitigation / workaround / operational guidance

工業與醫療場景常見的最佳實踐是：當正式 patch 需要較久時，先提供

* BIOS setting 調整
* feature disable
* network segmentation
* ACL / firewall rule
* service isolation
* upgrade path
* field notice
  這一點與 Siemens 工業場景、CISA/CVD 的實務精神一致，也很符合你前面提到 IEI 可能透過 BIOS、driver、software app 提供 mitigation 的情境。([Siemens][6])

---

## 4) 角色分工的最佳實踐範例

對 IEI，我建議把 PSIRT 的 RACI 定義成下面這樣，這是最實用的版本：

### PSIRT

負責 intake、case ownership、外部溝通、時程控管、CVE/CNA 協調、公告治理。這與 FIRST 對 PSIRT 核心服務的描述一致。([first.org][2])

### PM

負責產品識別、商業影響、客戶分層、EOL/EOS 判斷、ODM/OEM 協調、release priority。這對產品家族多的 IPC 廠尤其重要；否則 RD 修完也不知道先推給誰。此處屬依產品型企業最佳實踐的管理設計，但與 FIRST 的 stakeholder / service 視角相符。([first.org][4])

### RD

負責技術分析、root cause、修補設計、與供應商技術對接。Siemens 官方即明示漏洞處理由 ProductCERT 與負責的 development groups 協作完成。([Siemens][6])

### DQV / QA

負責 reproduction、regression test、版本驗證、證據保留、release gate。對硬體/韌體產品，這個角色不能省，因為 patch 可用不等於可量產、可穩定、可交付。這是工業產品廠的典型最佳實踐。([Siemens][6])

### SCM / Supplier Management

負責第三方零件/BOM/替代料/供應商狀態確認。這是 IPC/ODM 類公司相較純軟體商多出來的關鍵角色，與 ENISA 對供應鏈資安實務的方向一致。([歐洲網絡與信息安全局][8])

### Legal / PR / Sales

負責對外法律風險、客戶書面通知、公開聲明、研究員 recognition 或 bounty 條件核對。這些不是 PSIRT 主責，但成熟 PSIRT 一定會把它們納入流程節點。([first.org][2])

---

## 5) 指標怎麼設，才算「最佳實踐」

真正成熟的 PSIRT 不只看有沒有收信箱，而是看 KPI / KRI。常見的實務指標包括：

* 首次確認回覆時間
* triage 完成時間
* 可重現率
* 受理率 / 拒絕率與原因
* 第三方依賴案件比例
* 修補完成時間
* 公告發布時間
* 補丁可用率
* mitigation 先行比例
* 重複通報率
* 已知漏洞在售後客訴中的再出現率
  FIRST 的成熟度思維就是希望 PSIRT 從「有功能」走到「可量測、可改進」。([first.org][4])

對 IEI 這種公司，我會特別再加兩個：

* **涉及 ODM/OEM 客戶協調的案件比例**
* **涉及上游供應商依賴的案件比例**
  因為這兩項最能反映 industrial vendor 的真實治理難度。這是根據你前面整理的 IEI 產業鏈位置所做的實務延伸。([first.org][2])

---

## 6) 一個可直接套用的「最佳實踐範例」

若你要一句話定義 IEI 版 PSIRT 最佳實踐，我會寫成：

> IEI PSIRT 應建立一套以 ISO/IEC 29147 與 ISO/IEC 30111 為基礎、參照 FIRST PSIRT Services Framework 的產品漏洞處理機制；該機制應涵蓋公開通報入口、研究員協調、產品與版本影響分析、第三方供應鏈協調、修補與緩解措施開發、驗證與發布、ODM/OEM 客戶通知，以及可量測的持續改善機制。([NIST CSRC][1])

---

## 7) 我對 IEI 的建議：最值得抄的不是哪一家公司，而是哪一種組合

對 IEI 來說，最好的參考組合不是單抄 Cisco 或單抄 Microsoft，而是：

* **治理框架**：FIRST PSIRT Services Framework ([first.org][2])
* **標準骨架**：ISO/IEC 29147 + 30111（可參考 NIST 對兩者關係的說明）([NIST CSRC][1])
* **工業產品實務**：Siemens ProductCERT ([Siemens][6])
* **入口與協調揭露**：CISA VDP / Microsoft CVD ([CISA][9])
* **公告與固定發布節奏**：Cisco / Microsoft advisory discipline ([Cisco][5])

這樣的組合最適合你前面描述的 IEI：**中游系統整合型、B2B、供應鏈依賴重、產品線多、客製專案多**。([first.org][2])

## 摘要

* PSIRT 最佳實踐不是只有「收漏洞」，而是把 **揭露、修補、驗證、通知、公告、量測** 做成閉環。([NIST CSRC][1])
* 對 IEI 這類 IPC/ODM/OEM 製造商，最重要的是 **供應鏈協調、產品型號/BOM 影響分析、OEM 客戶通知、mitigation 先行機制**。([Siemens][6])
* 產業實務上，**Siemens ProductCERT** 最像工業產品廠可參考的範本；**Cisco / Microsoft** 則可作為政策公開、入口設計與 advisory 運作的參考。([Cisco][5])

我可以下一步直接幫你整理成「**IEI PSIRT Best Practice Blueprint**」一頁式架構，或轉成 **Vulnerability Disclosure Process 程序書章節大綱**。

[1]: https://csrc.nist.gov/projects/vulnerability-disclosure-guidelines/iso-pubs?utm_source=chatgpt.com "Vulnerability Disclosure Guidelines | CSRC"
[2]: https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1?utm_source=chatgpt.com "PSIRT Services Framework 1.1"
[3]: https://www.iso.org/obp/ui/?utm_source=chatgpt.com "ISO/IEC 29147:2018(en), Information technology"
[4]: https://www.first.org/standards/frameworks/psirts/psirt_maturity_document?utm_source=chatgpt.com "Product Security Incident Response Team (PSIRT) Maturity ..."
[5]: https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html?utm_source=chatgpt.com "Security Vulnerability Policy"
[6]: https://www.siemens.com/en-us/content/cert-services-vulnerability-process/?utm_source=chatgpt.com "Siemens Vulnerability Handling and Disclosure Process"
[7]: https://msrc.microsoft.com/create-report?utm_source=chatgpt.com "MSRC Researcher Portal"
[8]: https://www.enisa.europa.eu/publications/good-practices-for-supply-chain-cybersecurity?utm_source=chatgpt.com "Good Practices for Supply Chain Cybersecurity - ENISA"
[9]: https://www.cisa.gov/resources-tools/services/vulnerability-disclosure-policy-vdp-platform?utm_source=chatgpt.com "Vulnerability Disclosure Policy (VDP) Platform"
