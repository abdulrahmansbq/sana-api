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
            audio_file = DownloadingService(self.video_id[3:].replace("/", "")).download()
            self._update_frontend_status("downloaded")

           
            transcript_file = TranscribingService(
                audio_file=audio_file,
                file_name=self.video_id,
            ).transcribe(service_provider="whisper-api")
            
            opened_transcript = open(transcript_file, "r")
            saved_transcript = opened_transcript.read()
            opened_transcript.close()
        
            self._update_frontend_status("transcribed")

            EmbeddingService().embed_transcript(
                chrome_client=self.chroma_client,
                namespace_id=self.video_id,
                text_file=transcript_file,
            )

            self._update_frontend_status("completed", saved_transcript)

        except DownloadingException | EmbeddingException | TranscribingException as e:
            self._update_frontend_status("failed")
            return {"status": "Error", "message": e}

        self._cleanup()

        return {"status": "Success", "message": "Video embedded successfully"}

    def _cleanup(self):
        os.remove(settings.STORAGE_PATH + "temp/" + self.video_id[3:].replace("/", "") + ".txt")
        os.remove(settings.STORAGE_PATH + "temp/" + self.video_id[3:].replace("/", "") + ".mp3")

    def _update_frontend_status(self, status, transcript=None):
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
                },
                headers={"Authorization": "Bearer " + settings.LARAVEL_API_KEY},
            )
