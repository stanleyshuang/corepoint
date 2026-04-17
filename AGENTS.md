## 回覆語言
一律使用繁體中文回覆。

## 執行原則
執行 prompt 時，如有不清楚或規格不完整的地方，先停下來釐清；得到回應後再繼續進行。

## 執行後回饋
每次執行完 prompt 後，需提供可改進之處，至少包含以下項目：
- 不需特別寫出的內容
- 需要更仔細描述的規格
- 其他更好的建議

## Python 執行環境
```powershell
# Python 安裝路徑（已安裝）
$env:LocalAppData\Programs\Python\Python312\python.exe --version

# 專案虛擬環境位置
# C:\Users\stanleyhuang\github\stanleyshuang\corepoint\.venv

# 啟用虛擬環境
.\.venv\Scripts\Activate.ps1

# 驗證 Python / pip（建議在啟用 venv 後執行）
python --version
pip --version

# 若 python 指令受 WindowsApps alias 影響，請改用：
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```
