from core.exceptions.downloading_exception import DownloadingException
from core.settings import Settings
from yt_dlp import YoutubeDL


settings = Settings()

class DownloadingService:
    def __init__(
            self,
            video_id: str,
            service_provider: str = "youtube"
    ):
        self.video_id = video_id
        self.service_provider = service_provider


    def download(self):
        """
        Downloads the video from a service provider

        :return:
        """
        if self.service_provider == "youtube":
            return self._download_from_youtube()
        else:
            raise DownloadingException("Service provider is not supported")


    def _download_from_youtube(self):
        """
        Downloads the video from Youtube using youtube-dl

        :return:
        """
        video = self.video_id
        ydl_opts = {
            'outtmpl': settings.STORAGE_PATH + f"temp/{video}",
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video}"])
        return  settings.STORAGE_PATH + "temp/" + video + ".mp3"