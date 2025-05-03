# 🎵 YouTube 歌曲自動下載工具

本專案是一個以 Python 實作的自動化工具，根據 `歌單.txt` 批次搜尋 YouTube 上的歌曲，自動下載為 `.mp3` 並儲存至指定資料夾。

## 🚀 功能特點

- 📄 讀取本地 `歌單.txt`，逐行搜尋並下載歌曲
- 🔍 使用 Fuzzy Matching 自動選擇相似度最高的影片
- 🎧 轉換為 `.mp3` 音訊格式（使用 ffmpeg）
- 📂 可自訂輸出資料夾，支援 CLI 參數操作
- 🪵 支援 log 紀錄與失敗歌曲備份 (`log.txt`, `failed.txt`)

## 📦 環境需求

- Python 3.8+
- ffmpeg（Ubuntu 可使用 `sudo apt install ffmpeg` 安裝）

安裝 Python 套件：
```bash
pip install -r requirements.txt
```

## 🛠 使用方式

### ✅ CLI 執行方式（建議）

```bash
python download_music.py -i 歌單.txt -o downloads -l log.txt
```

支援參數如下：

| 參數 | 說明 |
|------|------|
| `-i`, `--input` | 指定歌單檔案，預設為 `歌單.txt` |
| `-o`, `--output` | 指定輸出資料夾，預設為 `downloads/` |
| `-l`, `--log` | 指定 log 檔案名稱，預設為 `log.txt` |
| `--dry-run` | 只模擬搜尋，不下載 |

### ✅ Docker 執行方式

```bash
docker run --rm -v "$PWD:/app" youtube-mp3-downloader   python download_music.py -i 歌單.txt -o downloads
```

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
├── Dockerfile              # Docker 容器執行設定
├── README.md               # 使用說明
└── .gitignore              # Git 忽略規則
```

## 🧠 進階方向

- 加入 MP3 ID3 metadata
- 使用 Docker Compose 自動掛載歌單與輸出路徑
- 實作 GUI 或 Web API 介面

## 📄 授權 License

MIT License

---

## 🙋‍♂️ 作者

Developed by [Kobayashi](https://github.com/a9722399100)
