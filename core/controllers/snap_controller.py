import httpx
from langchain_ibm import WatsonxLLM
import json
from jsonschema import validate
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

        docs = snapping_service.chunkify_text(self.transcript)

        for doc in docs:
            prompt = snapping_service.get_prompt(doc.page_content)

            snaps = self.model(prompt)
            if not snaps:
                continue

            with httpx.Client() as client:
                client.post(
                    settings.LARAVEL_ENDPOINT+"/api/snaps/store",
                    json={
                        "namespace_id": self.namespace_id,
                        "type": self.namespace_type,
                        "summary": snaps
                    },
                    headers={
                        "Authorization": "Bearer "+settings.LARAVEL_API_KEY
                    }
                    )
        return "Snaps generated successfully"

    def _validate_json(self, data):
        schema = {
            "type": "object",
            "properties": {
                "sentences": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1  # You can adjust the minimum number of items if needed
                }
            },
            "required": ["sentences"]
        }
        try:
            loaded_data = json.loads(data)
        except json.JSONDecodeError:
            return False

        if not validate(loaded_data, schema):
            return False
        return loaded_data