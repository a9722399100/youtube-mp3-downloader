import yt_dlp
from fuzzywuzzy import fuzz
import os
import re
import logging
import argparse

# === 解析命令列參數 ===
parser = argparse.ArgumentParser(description="YouTube 自動 mp3 下載工具")
parser.add_argument('-i', '--input', type=str, default='歌單.txt', help='指定歌單檔案路徑')
parser.add_argument('-o', '--output', type=str, default='downloads', help='指定輸出資料夾')
parser.add_argument('-l', '--log', type=str, default='log.txt', help='指定 log 檔案名稱')
parser.add_argument('--dry-run', action='store_true', help='只顯示搜尋結果不下載')
args = parser.parse_args()

DOWNLOAD_DIR = os.path.abspath(args.output)
LOG_FILE = args.log
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# === 設定 logging ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === 記錄失敗歌曲 ===
def record_failure(song_name):
    with open('failed.txt', 'a', encoding='utf-8') as f:
        f.write(song_name + '\n')

# === 清理檔案名稱 ===
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

    if args.dry_run:
        print(f"[Dry Run] 🔍 準備下載: {best_title} ({video_url})")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
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
    playlist_file = args.input
    if os.path.exists(playlist_file):
        print(f"📄 使用歌單檔案: {playlist_file}")
        download_from_text_file(playlist_file)
    else:
        print(f"❌ 找不到指定的歌單檔案: {playlist_file}")

if __name__ == "__main__":
    main()

