from pytube import YouTube

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        if not stream:
            print("No suitable stream found!")
            return None
        downloaded_file = stream.download(output_path=output_path)
        print("Downloaded to:", downloaded_file)
        return downloaded_file
    except Exception as e:
        print("Error downloading video:", e)
        return None

url = "https://youtu.be/quKgo3ChvWY?si=6YobkdUlPiaqNPFP"
download_youtube_video(url, "./downloads")
