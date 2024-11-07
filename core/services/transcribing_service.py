import whisper
from openai import Audio

from core.exceptions.transcribing_exception import TranscribingException
from core.settings import Settings

settings = Settings()


class TranscribingService:
    TRANSCRIBING_MODE_STORE = 1
    TRANSCRIBING_MODE_RETURN = 2

    def __init__(
        self, audio_file: str, file_name: str = None, mode=TRANSCRIBING_MODE_STORE
    ):
        self.audio_file = audio_file
        self.mode = mode
        self.file_name = file_name
        self.openai_client = Audio()

    def transcribe(self, service_provider: str = "whisper"):
        """
        Transcribes the audio file

        :return:
        """
        if service_provider == "whisper":
            return self._transcribe_with_whisper()
        elif service_provider == "whisper-api":
            return self._transcribe_with_whisper_api()
        else:
            raise TranscribingException("Service provider is not supported")

    def _transcribe_with_whisper(self):
        """
        Transcribes the audio file using whisper

        :return:
        """
        whisper_client = whisper.load_model(
            settings.WHISPER_MODEL, device=settings.WHISPER_DEVICE
        )
        result = whisper_client.transcribe(self.audio_file)
        transcript = result["text"]
        if self.mode == self.TRANSCRIBING_MODE_STORE:
            return self._store_in_text(transcript)
        return transcript

    def _transcribe_with_whisper_api(self):
        """
        Transcribes the audio file using whisper api

        :return:
        """
        audio_file = open(self.audio_file, "rb")

        result = self.openai_client.transcribe(
            api_key=settings.OPENAI_API_KEY,
            model="whisper-1",
            file=audio_file,
        )
        transcript = result["text"]
        if self.mode == self.TRANSCRIBING_MODE_STORE:
            return self._store_in_text(transcript)
        return transcript

    def _store_in_text(self, content):
        """
        Stores the transcript in a text file

        :param content:
        :return:
        """
        print(content)
        with open(
            settings.STORAGE_PATH + "temp/" + self.file_name + ".txt", "w"
        ) as text_file:
            text_file.write(content)
        return settings.STORAGE_PATH + "temp/" + self.file_name + ".txt"
