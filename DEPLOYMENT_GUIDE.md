# LINE Bot Webhook 永久部署指南

## 📦 專案資訊

**GitHub 儲存庫**: https://github.com/MUXUPilates/linebot-webhook-deploy

所有部署所需的檔案已準備完成並上傳至 GitHub，您可以直接使用此儲存庫進行部署。

---

## 🚀 方案一：Render 部署（推薦，完全免費）

### 步驟 1：註冊 Render 帳號

1. 前往 [Render](https://render.com/)
2. 點擊 **Get Started for Free**
3. 選擇使用 **GitHub** 帳號註冊（最方便）
4. 授權 Render 存取您的 GitHub 帳號

### 步驟 2：建立 Web Service

1. 登入後，點擊右上角的 **New +** 按鈕
2. 選擇 **Web Service**
3. 選擇 **Connect a repository**
4. 找到並選擇 `MUXUPilates/linebot-webhook-deploy` 儲存庫
5. 如果看不到儲存庫，點擊 **Configure account** 授權存取

### 步驟 3：設定部署參數

在設定頁面填入以下資訊：

- **Name**: `linebot-webhook` (或您喜歡的名稱)
- **Region**: 選擇 `Singapore` (最接近台灣)
- **Branch**: `master`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT linebot_app:app`

### 步驟 4：設定環境變數

在 **Environment Variables** 區塊，點擊 **Add Environment Variable**，新增以下三個變數：

| Key | Value |
|-----|-------|
| `LINE_CHANNEL_ACCESS_TOKEN` | `您的 LINE Channel Access Token` |
| `LINE_CHANNEL_SECRET` | `您的 LINE Channel Secret` |
| `OPENAI_API_KEY` | `您的 OpenAI API Key` |

### 步驟 5：選擇免費方案

- **Instance Type**: 選擇 **Free**
- 免費方案限制：
  - 閒置 15 分鐘後會休眠
  - 首次喚醒需要 30-60 秒
  - 每月 750 小時免費運行時間

### 步驟 6：部署

1. 點擊 **Create Web Service**
2. 等待 3-5 分鐘完成部署
3. 部署完成後，您會看到一個 URL，格式如：`https://linebot-webhook.onrender.com`

### 步驟 7：設定 LINE Webhook

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Channel
3. 在 **Messaging API** 頁籤中找到 **Webhook URL**
4. 填入：`https://你的render網址.onrender.com/callback`
5. 點擊 **Verify** 確認連線成功
6. 啟用 **Use webhook**

---

## 🚂 方案二：Railway 部署（推薦，每月 $5 免費額度）

### 步驟 1：註冊 Railway 帳號

1. 前往 [Railway](https://railway.app/)
2. 點擊 **Login** 使用 GitHub 帳號登入

### 步驟 2：建立新專案

1. 點擊 **New Project**
2. 選擇 **Deploy from GitHub repo**
3. 選擇 `MUXUPilates/linebot-webhook-deploy` 儲存庫

### 步驟 3：設定環境變數

1. 在專案頁面，點擊您的服務
2. 切換到 **Variables** 頁籤
3. 新增以下環境變數：

```
LINE_CHANNEL_ACCESS_TOKEN=您的_LINE_Channel_Access_Token
LINE_CHANNEL_SECRET=您的_LINE_Channel_Secret
OPENAI_API_KEY=您的_OpenAI_API_Key
```

### 步驟 4：啟用公開網域

1. 切換到 **Settings** 頁籤
2. 找到 **Networking** 區塊
3. 點擊 **Generate Domain**
4. 複製產生的 URL

### 步驟 5：設定 LINE Webhook

將 Railway 提供的 URL + `/callback` 設定到 LINE 官方後台。

---

## 🐳 方案三：使用 Docker 部署到任何平台

### Dockerfile

如果您想使用 Docker 部署，可以建立以下 Dockerfile：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY linebot_app.py .

ENV PORT=5000

CMD gunicorn -w 4 -b 0.0.0.0:$PORT linebot_app:app
```

### 建置和執行

```bash
# 建置映像
docker build -t linebot-webhook .

# 執行容器
docker run -p 5000:5000 \
  -e LINE_CHANNEL_ACCESS_TOKEN="您的TOKEN" \
  -e LINE_CHANNEL_SECRET="您的SECRET" \
  -e OPENAI_API_KEY="您的API_KEY" \
  linebot-webhook
```

---

## 📝 功能說明

### 核心邏輯

當使用者傳送訊息給 LINE Bot 時：

1. **前綴檢查**：檢查訊息是否以 `.` (半形句點) 開頭
2. **字串處理**：如果是 `.` 開頭，僅移除第一個字元，保留後面所有內容（包含空白、換行、連續的點）
3. **AI 處理**：將處理後的內容傳送給 OpenAI GPT-5 模型
4. **回覆**：將 AI 的回應透過 LINE Reply API 傳回給使用者

### 測試範例

| 使用者輸入 | 傳送給 AI | 說明 |
|-----------|----------|------|
| `.你好` | `你好` | 移除第一個點 |
| `.      你好` | `      你好` | 保留所有空白 |
| `...........` | `..........` | 保留剩下的點 |
| `.你好\n世界` | `你好\n世界` | 保留換行 |
| `你好` | (不處理) | 沒有點開頭，不回應 |

---

## 🔧 故障排除

### 問題 1：LINE Webhook 驗證失敗

**解決方法**：
- 確認 URL 格式正確：`https://你的網址/callback`
- 確認服務已成功部署並運行
- 檢查環境變數是否正確設定

### 問題 2：Bot 沒有回應

**檢查項目**：
1. 確認訊息是以 `.` 開頭
2. 檢查 Render/Railway 的日誌，查看是否有錯誤訊息
3. 確認 OpenAI API Key 是否有效
4. 確認 LINE Channel Access Token 是否正確

### 問題 3：Render 免費方案休眠

**解決方法**：
- 使用 [UptimeRobot](https://uptimerobot.com/) 每 5 分鐘 ping 一次您的服務
- 或升級到 Render 付費方案（每月 $7 起）

### 問題 4：OpenAI API 錯誤

**可能原因**：
- API Key 無效或過期
- 帳號額度不足
- `gpt-5` 模型不可用（可能需要改為 `gpt-4` 或 `gpt-3.5-turbo`）

---

## 📊 成本比較

| 平台 | 免費方案 | 限制 | 推薦度 |
|-----|---------|------|-------|
| **Render** | ✅ 完全免費 | 閒置 15 分鐘休眠 | ⭐⭐⭐⭐⭐ |
| **Railway** | ✅ $5/月額度 | 約 500 小時/月 | ⭐⭐⭐⭐ |
| **Fly.io** | ✅ 有限免費 | 需信用卡 | ⭐⭐⭐ |
| **Heroku** | ❌ 無免費方案 | 最低 $5/月 | ⭐⭐ |

---

## 🎯 建議部署流程

**最簡單的方式**：

1. ✅ 使用 GitHub 帳號註冊 Render
2. ✅ 連接 `MUXUPilates/linebot-webhook-deploy` 儲存庫
3. ✅ 設定三個環境變數
4. ✅ 選擇免費方案
5. ✅ 部署完成，取得 URL
6. ✅ 將 URL + `/callback` 設定到 LINE 官方後台

**總耗時**：約 10-15 分鐘

---

## 📞 需要協助？

如果您在部署過程中遇到任何問題，可以：

1. 檢查 Render/Railway 的部署日誌
2. 確認環境變數是否正確設定
3. 測試 Webhook URL 是否可以正常存取（訪問 `https://你的網址/` 應該顯示 "LINE Bot Webhook is running!"）

---

## 🔐 安全提醒

⚠️ **重要**：您的 API 金鑰已經暴露在此文件中，建議部署完成後：

1. 前往 LINE Developers Console 重新生成 Channel Access Token
2. 前往 OpenAI 平台重新生成 API Key
3. 在 Render/Railway 更新環境變數
4. 刪除此文件或將金鑰替換為 `***`

---

**祝您部署順利！** 🎉
