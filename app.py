from flask import Flask, render_template, request, send_from_directory, jsonify
from yt_downloader import download_video, progress_dict
from threading import Thread
import uuid
import os

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")

# Store mapping: download_id -> filename
download_files = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        audio_only = request.form.get("audio_only") == "on"

        if not url:
            return render_template("index.html", error="Please enter a valid YouTube URL")

        download_id = str(uuid.uuid4())
        progress_dict[download_id] = '0%'
        
        def run_download():
            try:
                filename = download_video(url, audio_only, download_id)
                download_files[download_id] = filename
            except Exception as e:
                progress_dict[download_id] = 'error'

        Thread(target=run_download).start()

        return render_template("index.html", download_id=download_id)

    return render_template("index.html")

@app.route("/progress/<download_id>")
def progress(download_id):
    return jsonify(progress=progress_dict.get(download_id, '0%'))

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
