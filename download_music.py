import yt_dlp
from fuzzywuzzy import fuzz
import os
import re
import logging

# === 準備資料夾 ===
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === 設定 logging ===
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === 記錄失敗歌曲 ===
def record_failure(song_name):
    with open('failed.txt', 'a', encoding='utf-8') as f:
        f.write(song_name + '\n')

# === 清理檔案名稱（移除非法字元並取代空白）===
def clean_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*⧸]', '', filename)
    filename = filename.replace(' ', '_').replace('　', '_')
    return filename.strip()

# === 搜尋最相近影片 ===
def search_best_match(song_name):
    logging.info(f"搜尋歌曲: {song_name}")
    ydl_opts = {'quiet': True, 'default_search': 'ytsearch5'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_results = ydl.extract_info(song_name, download=False)
        except Exception as e:
            logging.error(f"搜尋失敗: {song_name} - {e}")
            return None, None

    if 'entries' not in search_results or not search_results['entries']:
        logging.warning(f"找不到任何影片: {song_name}")
        return None, None

    best_match = None
    best_score = 0
    best_url = None

    for entry in search_results['entries']:
        title = entry['title']
        url = entry['webpage_url']
        score = fuzz.ratio(song_name.lower(), title.lower())
        if score > best_score:
            best_score = score
            best_match = title
            best_url = url

    # 避免低相似度誤判（可依需求調整門檻）
    if best_score < 60:
        logging.warning(f"無合適影片匹配: {song_name}（最高相似度 {best_score}%）")
        return None, None

    logging.info(f"選定影片: {best_match}（相似度: {best_score}%）")
    return best_match, best_url

# === 下載影片並轉 MP3 ===
def download_song(song_name):
    best_title, video_url = search_best_match(song_name)

    if not video_url:
        logging.error(f"未取得影片連結: {song_name}")
        record_failure(song_name)
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # 如需指定 ffmpeg 位置可啟用以下行
        # 'ffmpeg_location': '/usr/bin/ffmpeg',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_title = info.get('title', 'unknown')
            final_filename = clean_filename(downloaded_title) + ".mp3"
            final_path = os.path.join(DOWNLOAD_DIR, final_filename)

            if os.path.exists(final_path):
                logging.info(f"下載成功: {final_filename}")
            else:
                raise FileNotFoundError(f"找不到下載檔案：{final_path}")

    except Exception as e:
        logging.error(f"下載失敗: {song_name} - {e}")
        record_failure(song_name)

# === 讀取歌單 ===
def download_from_text_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        songs = file.readlines()

    for song in songs:
        song_name = song.strip()
        if song_name:
            print(f"\n🎶 開始下載: {song_name}")
            download_song(song_name)

# === 主程式進入點 ===
def main():
    playlist_file = os.path.join(os.path.dirname(__file__), "歌單.txt")
    if os.path.exists(playlist_file):
        print(f"📄 找到歌單檔案: {playlist_file}")
        download_from_text_file(playlist_file)
    else:
        print("❌ 沒有找到 '歌單.txt'，請確認檔案存在")

if __name__ == "__main__":
    main()

