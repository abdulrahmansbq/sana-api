from yt_dlp import YoutubeDL
import requests

def get_mp3_url(video_url):
    """
    Extracts the direct MP3 URL of a YouTube video without downloading the file locally.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "noplaylist": True,
        "extractaudio": True,
        "quiet": True,
        "skip_download": True,  # Prevents local download
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        audio_url = info['url']
        
    return audio_url

def stream_audio(mp3_url):
    """
    Streams the audio from the direct MP3 URL using requests.
    """
    response = requests.get(mp3_url, stream=True)
    
    # Process or save the audio stream as needed
    with open("output.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    print("Audio saved as output.mp3")

# Example usage
video_url = 'https://www.youtube.com/watch?v=QX3WF2Bba-s'  # Replace with the actual video ID
mp3_url = get_mp3_url(video_url)
print("MP3 Direct URL:", mp3_url)

# Stream and save the audio
stream_audio(mp3_url)