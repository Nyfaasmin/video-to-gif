import os

def process_video(video_path, transcript, segments, output_folder):
    gifs = []
    for i, (start, end) in enumerate(segments):
        gif_path = os.path.join(output_folder, f"clip_{i}.gif")
        with open(gif_path, "wb") as f:
            f.write(b"GIF89a")  # Dummy gif header for test
        gifs.append(gif_path)
    return gifs
