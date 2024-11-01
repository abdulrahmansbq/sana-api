from core.exceptions.transcribing_exception import TranscribingException
from core.settings import Settings
import whisper


settings = Settings()


class TranscribingService:
    TRANSCRIPT_MODE_STORE = 1
    TRANSCRIPT_MODE_RETURN = 2



    def __init__(
            self,
            audio_file: str,
            file_name: str = None,
            mode = TRANSCRIPT_MODE_STORE
    ):
        self.audio_file = audio_file
        self.mode = mode
        self.file_name = file_name


    def transcribe(self, service_provider: str = "whisper"):
        """
        Transcribes the audio file

        :return:
        """
        if service_provider == "whisper":
            return self._transcribe_with_whisper()
        else:
            raise TranscribingException("Service provider is not supported")


    def _transcribe_with_whisper(self):
        """
        Transcribes the audio file using whisper

        :return:
        """
        whisper_client = whisper.load_model(settings.WHISPER_MODEL, device=settings.WHISPER_DEVICE)
        result = whisper_client.transcribe(self.audio_file)
        transcript = result["text"]
        if self.mode == self.TRANSCRIPT_MODE_STORE:
            return self._store_in_text(transcript)
        return transcript


    def _store_in_text(self, content):
        """
        Stores the transcript in a text file

        :param content:
        :return:
        """
        with open(settings.STORAGE_PATH + "temp/" + self.file_name + ".txt", "w") as text_file:
            text_file.write(content)
        return settings.STORAGE_PATH + "temp/" + self.file_name + ".txt"