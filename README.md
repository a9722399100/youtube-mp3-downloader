# 🎵 YouTube 歌曲自動下載工具

本專案是一個以 Python 實作的自動化工具，根據 `歌單.txt` 批次搜尋 YouTube 上的歌曲，自動下載為 `.mp3` 並儲存至 `downloads/` 資料夾。

## 🚀 功能特點

- 📄 讀取本地 `歌單.txt`，逐行搜尋並下載歌曲
- 🔍 使用 Fuzzy Matching 自動選擇相似度最高的影片
- 🎧 轉換為 `.mp3` 音訊格式（使用 ffmpeg）
- 📂 自動存入 `downloads/` 並清理非法檔名
- 🪵 支援 log 紀錄與失敗歌曲備份 (`log.txt`, `failed.txt`)

## 📦 環境需求

- Python 3.8+
- ffmpeg（Ubuntu 可使用 `sudo apt install ffmpeg` 安裝）

安裝 Python 套件：
```bash
pip install -r requirements.txt
```

## 🛠 使用方式

1. 將你的歌名清單寫入 `歌單.txt`，例如：
```
陪我看日出（蔡淳佳）
碼頭惜別（葉啟田）
```

2. 執行程式：
```bash
python download_music.py
```

3. 成功轉檔的 mp3 檔案將會出現在 `downloads/` 資料夾。

## 📁 專案結構簡述

```
.
├── download_music.py       # 主程式
├── 歌單.txt                 # 歌曲清單（使用者輸入）
├── downloads/              # 儲存下載檔案
│   └── .keep               # 保留資料夾
├── log.txt                 # 執行記錄
├── failed.txt              # 下載失敗歌曲
├── requirements.txt        # 套件清單
├── README.md               # 使用說明
└── .gitignore              # Git 忽略規則
```

## 🧠 進階方向（可選）

- 將工具包裝成 GUI
- 使用 Docker 容器化
- 加入 MP3 ID3 metadata
- 實作 Web API 版本

## 📄 授權 License

MIT License

---

## 🙋‍♂️ 作者

Developed by [Kobayashi](https://github.com/a9722399100)
