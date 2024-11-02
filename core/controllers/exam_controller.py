from langchain_ibm import WatsonxLLM
from core.services.chunking_service import ChunkingService
from core.services.exam_service import ExamService
from core.settings import Settings

settings = Settings()




class ExamController:
    def __init__(
            self,
            namespace_id,
            namespace_type,
            transcript
    ):
        self.namespace_id = namespace_id
        self.namespace_type = namespace_type
        self.transcript = transcript
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
        Generates the questions

        :return:
        """

        exam_service = ExamService()

        docs = ChunkingService().chunkify_text(transcript=self.transcript, chunking_mode=ChunkingService.CHUNKING_FROM_TEXT)

        for doc in docs:
            prompt = exam_service.get_prompt(doc.page_content)

            questions = self.model(prompt)
            if not questions:
                continue

            if not exam_service.validate_json(questions):
                continue

            exam_service.send_to_frontend(questions=questions, namespace_id=self.namespace_id, namespace_type=self.namespace_type)

        return "Questions generated successfully"
