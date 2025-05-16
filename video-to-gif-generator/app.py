from flask import Flask, render_template, request, send_file
import os
from utils.whisper_transcriber import transcribe_video
from utils.video_processor import process_video

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
GIF_FOLDER = "static/gifs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GIF_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    gifs = []
    if request.method == "POST":
        prompt = request.form["prompt"]
        file = request.files["video"]
        if file:
            video_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(video_path)
            transcript, segments = transcribe_video(video_path, prompt)
            gifs = process_video(video_path, transcript, segments, GIF_FOLDER)
    return render_template("index.html", gifs=gifs)

if __name__ == "__main__":
    app.run(debug=True)
