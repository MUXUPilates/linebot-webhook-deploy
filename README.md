# LINE Bot Webhook 部署指南

這是一個整合 OpenAI API 的 LINE Bot Webhook 應用程式，使用 Flask 框架開發。

## 功能說明

- 當使用者傳送以 `.` (半形句點) 開頭的訊息時，系統會移除第一個字元，並將剩餘內容傳送給 OpenAI GPT-5 模型
- AI 的回應會透過 LINE Reply API 自動傳回給使用者
- 保留所有空白、換行和特殊字元

## 檔案結構

```
.
├── linebot_app.py      # 主應用程式
├── requirements.txt    # Python 套件依賴
├── render.yaml         # Render 部署配置
├── railway.json        # Railway 部署配置
├── .gitignore          # Git 忽略檔案
└── README.md           # 說明文件
```

## 永久部署方案

### 方案 1：Render（推薦，免費方案）

1. 前往 [Render](https://render.com/) 註冊帳號
2. 點擊 "New +" → "Web Service"
3. 連接您的 GitHub 儲存庫（需先將程式碼上傳至 GitHub）
4. 設定如下：
   - **Name**: linebot-webhook
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT linebot_app:app`
5. 點擊 "Create Web Service"
6. 部署完成後，Render 會提供一個永久 URL，格式如：`https://linebot-webhook.onrender.com`
7. 將 `https://linebot-webhook.onrender.com/callback` 設定到 LINE 官方後台

**注意**：免費方案會在閒置 15 分鐘後休眠，首次喚醒需要 30-60 秒。

### 方案 2：Railway（推薦，免費額度）

1. 前往 [Railway](https://railway.app/) 註冊帳號
2. 點擊 "New Project" → "Deploy from GitHub repo"
3. 連接您的 GitHub 儲存庫
4. Railway 會自動偵測 Python 專案並部署
5. 在 Settings 中啟用 "Generate Domain" 以取得公開 URL
6. 將 URL + `/callback` 設定到 LINE 官方後台

**注意**：免費方案每月有 $5 USD 的使用額度，約可運行 500 小時。

### 方案 3：Fly.io（進階，需信用卡）

1. 前往 [Fly.io](https://fly.io/) 註冊帳號
2. 安裝 Fly CLI：`curl -L https://fly.io/install.sh | sh`
3. 登入：`flyctl auth login`
4. 在專案目錄執行：`flyctl launch`
5. 依照提示完成部署
6. 取得 URL 並設定到 LINE 官方後台

### 方案 4：Heroku（付費）

1. 前往 [Heroku](https://heroku.com/) 註冊帳號
2. 安裝 Heroku CLI
3. 在專案目錄執行：
   ```bash
   heroku login
   heroku create linebot-webhook
   git push heroku main
   ```
4. 取得 URL 並設定到 LINE 官方後台

## 本地測試

```bash
# 建立虛擬環境
python3 -m venv linebot_env
source linebot_env/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 啟動應用程式
python linebot_app.py
```

## 環境變數（選用）

如果您想使用環境變數而非寫死在程式碼中，可以設定：

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`
- `OPENAI_API_KEY`

## 測試範例

- 輸入：`.你好` → AI 收到：`你好`
- 輸入：`.      你好` → AI 收到：`      你好` (保留空白)
- 輸入：`...........` → AI 收到：`..........` (保留剩下的點)

## 技術支援

如有問題，請檢查：
1. LINE Channel Access Token 和 Secret 是否正確
2. OpenAI API Key 是否有效
3. Webhook URL 是否正確設定到 LINE 官方後台
4. 檢查部署平台的日誌以排查錯誤
