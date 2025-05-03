FROM python:3.10-slim

# 安裝 ffmpeg（轉 mp3 會用到）
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安裝 Python 套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式與歌單
COPY download_music.py .
COPY 歌單.txt .

CMD ["python", "download_music.py"]
