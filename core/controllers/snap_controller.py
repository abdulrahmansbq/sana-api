from langchain_ibm import WatsonxLLM
from core.services.chunking_service import ChunkingService
from core.services.snapping_service import SnappingService
from core.settings import Settings

settings = Settings()




class SnapController:
    def __init__(
            self,
            namespace_id,
            transcript,
            namespace_type
    ):
        self.namespace_id = namespace_id
        self.transcript = transcript
        self.namespace_type = namespace_type
        self.model = WatsonxLLM(
            model_id=settings.WATSONX_MODEL_ID,
            url=settings.WATSONX_URL,
            project_id=settings.WATSONX_PROJECT_ID,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 500,
                "repetition_penalty": 1.2
            },
            space_id=settings.WATSONX_SPACE_ID
        )

    async def generate(self):
        """
        Generates the snaps

        :return:
        """

        snapping_service = SnappingService()

        docs = ChunkingService().chunkify_text(transcript=self.transcript, chunking_mode=ChunkingService.CHUNKING_FROM_TEXT)

        for doc in docs:
            prompt = snapping_service.get_prompt(doc.page_content)

            snaps = self.model(prompt)
            if not snaps:
                continue

            if not snapping_service.validate_json(snaps):
                continue

            snapping_service.send_to_frontend(snaps=snaps, namespace_id=self.namespace_id, namespace_type=self.namespace_type)
        return "Snaps generated successfully"
