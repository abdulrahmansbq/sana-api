from datetime import timedelta
from yt_dlp import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from core.exceptions.downloading_exception import DownloadingException
from core.settings import Settings

settings = Settings()

class DownloadingService:
    def __init__(self, video_id: str, service_provider: str = "youtube"):
        self.video_id = video_id
        self.service_provider = service_provider

    def download(self):
        if self.service_provider == "youtube":
            return self._download_from_youtube()
        else:
            raise DownloadingException("Service provider is not supported")

    def _download_from_youtube(self):
        video = self.video_id
        video_url = f"https://www.youtube.com/watch?v={video}"
        
        chrome_options = Options()
        # chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })

        def human_like_wait(min_delay=1, max_delay=3):
            time.sleep(random.uniform(min_delay, max_delay))

        try:
            driver.get(video_url)
            human_like_wait(2, 5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            human_like_wait(2, 5)

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": settings.STORAGE_PATH + f"temp/{video}",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "http_headers": {
                    "User-Agent": chrome_options.arguments[-1],
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1"
                },
                # "cookiefile": "/home/cookies.txt"  # Update with path to your exported cookies file
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                video_title = info_dict.get("title", "Unknown Title")
                video_duration_seconds = info_dict.get("duration", 0)
                video_duration_formatted = str(timedelta(seconds=video_duration_seconds))
                ydl.download([video_url])

        finally:
            driver.quit()

        return {
            "file_path": settings.STORAGE_PATH + f"temp/{video}.mp3",
            "title": video_title,
            "duration": video_duration_formatted,
            "duration_seconds": video_duration_seconds,
        }
