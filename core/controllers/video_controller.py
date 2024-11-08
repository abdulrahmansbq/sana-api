import os

import chromadb
import httpx
from chromadb.errors import InvalidCollectionException

from core.exceptions.downloading_exception import DownloadingException
from core.exceptions.embedding_exception import EmbeddingException
from core.exceptions.transcribing_exception import TranscribingException
from core.services.downloading_service import DownloadingService
from core.services.embedding_service import EmbeddingService
from core.services.transcribing_service import TranscribingService
from core.settings import Settings

settings = Settings()


class VideoController:
    def __init__(self, video_id: str, response):
        self.video_id = video_id
        self.response = response
        self.chroma_client = chromadb.PersistentClient(
            path=settings.STORAGE_PATH + "chroma/"
        )

    async def embed(self):
        """
        Embeds the video in the database

        :return:
        """
        print("In embed: " + self.video_id)
        # self.chroma_client.delete_collection(self.video_id)
        try:
            collection = self.chroma_client.get_collection(self.video_id[3:].replace("/", ""))
            return {"status": "Error", "message": "Namespace already exists"}
        except InvalidCollectionException:
            pass

        try:
            # Download the audio
            downloader = DownloadingService(self.video_id[3:].replace("/", ""))
            # Download the audio and get both file path and title
            audio_data = downloader.download()
            # Access the file path and title from the returned dictionary
            file_path = audio_data.get("file_path")
            title = audio_data.get("title")
            duration = audio_data.get("duration")
            duration_seconds = audio_data.get("duration_seconds")

            # Notify the frontend that the audio has been downloaded
            self._update_frontend_status("downloaded")

            # Transcribe the audio
            transcript_file = TranscribingService(
                audio_file=file_path,
                file_name=self.video_id,
            ).transcribe(service_provider="whisper-api")
            
            # Open the transcript file and read its contents
            opened_transcript = open(transcript_file, "r")
            saved_transcript = opened_transcript.read()
            opened_transcript.close()
        
            # Notify the frontend that
            self._update_frontend_status("transcribed")

            # Embed the transcript
            EmbeddingService().embed_transcript(
                chrome_client=self.chroma_client,
                namespace_id=self.video_id,
                text_file=transcript_file,
            )

            # Notify the frontend that the video has been embedded
            self._update_frontend_status("completed", saved_transcript, title, duration_seconds)

        except DownloadingException | EmbeddingException | TranscribingException as e:
            self._update_frontend_status("failed")
            return {"status": "Error", "message": e}

        self._cleanup()

        return {"status": "Success", "message": "Video embedded successfully"}

    def _cleanup(self):
        os.remove(settings.STORAGE_PATH + "temp/" + self.video_id[3:].replace("/", "") + ".txt")
        os.remove(settings.STORAGE_PATH + "temp/" + self.video_id[3:].replace("/", "") + ".mp3")

    def _update_frontend_status(self, status, transcript=None, title=None, duration=None):
        """
        Notifies the frontend

        :return:
        """
        with httpx.Client(verify=False) as client:
            response = client.post(
                settings.LARAVEL_ENDPOINT + "/api/videos/" + self.video_id[3:].replace("/", "") + "/status",
                json={
                    "status": status,
                    "transcript": transcript,
                    "title": title,
                    "duration": duration,
                },
                headers={"Authorization": "Bearer " + settings.LARAVEL_API_KEY},
            )
