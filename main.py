from flask import Flask, request, jsonify, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)

PORT = 8000
COOKIES_FILE = "cookies.txt"

SUPPORTED_APPS = [
    "YouTube", "YouTube Shorts", "Instagram", "Facebook", "Twitter (X)",
    "TikTok", "Vimeo", "SoundCloud", "Twitch", "Dailymotion",
    "Likee", "Reddit", "Pinterest", "Snapchat", "Bilibili",
    "Rumble", "VK", "OK.ru", "IMDB Trailers", "Streamable"
]

def download_video(url, is_short=False):
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'outtmpl': filename,
        'format': 'best',
        'cookiefile': COOKIES_FILE,
        'quiet': True,
        'no_warnings': True,
    }

    if is_short:
        ydl_opts['format'] = 'best[height<=720]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename

@app.route("/")
def index():
    return jsonify({
        "info": "🎬 YouTube & Social Media Video Downloader API (Flask)",
        "routes": {
            "/down?url=": "Download full video",
            "/shortdown?url=": "Download Shorts, Reels, etc.",
            "/services": "List supported platforms"
        },
        "cookies_used": True,
        "port": PORT
    })

@app.route("/down")
def down():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    try:
        path = download_video(url)
        return send_file(path, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/shortdown")
def shortdown():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    try:
        path = download_video(url, is_short=True)
        return send_file(path, as_attachment=True, download_name="short_video.mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/services")
def services():
    return jsonify({
        "supported_apps": SUPPORTED_APPS,
        "total_supported": len(SUPPORTED_APPS),
        "note": "Many other platforms are also supported via yt-dlp."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
