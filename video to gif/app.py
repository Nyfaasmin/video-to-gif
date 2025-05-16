from flask import Flask, render_template, request
import os
from utils.yt_downloader import download_youtube_video
from utils.whisper_transcriber import transcribe
from utils.gif_generator import get_matching_segments, make_gif
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    gifs = []
    if request.method == 'POST':
        prompt = request.form['prompt']
        if request.form['youtube_url']:
            video_path = download_youtube_video(request.form['youtube_url'], UPLOAD_FOLDER)
        elif request.files['video_file']:
            file = request.files['video_file']
            filename = secure_filename(file.filename)
            video_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(video_path)
        else:
            return "Please provide a video.", 400

        transcript, segments = transcribe(video_path)
        matches = get_matching_segments(segments, prompt)
        gifs = make_gif(video_path, matches)

    return render_template('index.html', gifs=gifs)

if __name__ == '__main__':
    app.run(debug=True)
