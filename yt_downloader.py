import os
import yt_dlp
from threading import Thread

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# In-memory dictionary to track progress
progress_dict = {}

def download_video(url, audio_only=False, download_id=None):
    """
    Download video or audio and update progress_dict[download_id] in %
    """
    def progress_hook(d):
        if download_id:
            if d['status'] == 'downloading':
                progress_dict[download_id] = d.get('_percent_str', '0%').strip()
            elif d['status'] == 'finished':
                progress_dict[download_id] = '100%'

    ydl_opts = {
        'format': 'bestaudio+bestaudio/best' if audio_only else 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor' if not audio_only else 'FFmpegExtractAudio',
            'preferedformat': 'mp4' if not audio_only else 'mp3'
        }],
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if audio_only:
            filename = os.path.splitext(filename)[0] + ".mp3"

        if download_id:
            progress_dict[download_id] = '100%'

        return os.path.basename(filename)
