from pytube import YouTube
from pytube import request

def patched_execute_request(request_obj, timeout=None):
    request_obj.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    return request._execute_request_original(request_obj, timeout)

request._execute_request_original = request._execute_request
request._execute_request = patched_execute_request

url = "https://www.youtube.com/shorts/MWY1wApWPvc?si=IdZFNIXTsnmRhH2U"  # Use any valid public video URL here

try:
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
    print(f"Title: {yt.title}")
    print(f"Stream itag: {stream.itag}")
except Exception as e:
    print(f"Error: {e}")
