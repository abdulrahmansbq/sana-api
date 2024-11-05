import json
import httpx
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from langchain_core.prompts import PromptTemplate
from core.settings import Settings

settings = Settings()


class ExamService:
    def __init__(self):
        pass



    def get_prompt(self, context):
        """
        Gets the message

        :param context: The context
        :return: The message
        """

        prompt_file = open(settings.PROMPTS_PATH + "exam_prompt.txt", "r")

        prompt = prompt_file.read()

        template = PromptTemplate.from_template(prompt)

        processed_prompt = template.format(
            context=context,
            json_format='[\n{\n"question": "السؤال",\n"A": "الخيار الأول",\n"B": "الخيار الثاني",\n"C": "الخيار الثالث",\n"D": "الخيار الرابع",\n"answer": "A, B, C, or D"\n},\n\n]'
        )


        return processed_prompt


    def validate_json(self, data):
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "A": {"type": "string"},
                    "B": {"type": "string"},
                    "C": {"type": "string"},
                    "D": {"type": "string"},
                    "answer":  {
                        "enum": ["A", "B", "C", "D"]  # Ensures answer can only be one of these values
                    }
                },
                "required": ["question", "A", "B", "C", "D", "answer"]
            }
        }
        try:
            loaded_data = json.loads(data)
        except json.JSONDecodeError:
            return False

        try:
            validate(instance=loaded_data, schema=schema)
            return loaded_data
        except ValidationError as e:
            return False

    def send_to_frontend(self, namespace_id, namespace_type, questions):
        with httpx.Client(verify=False) as client:
            client.post(
                settings.LARAVEL_ENDPOINT+"/api/questions/store",
                json={
                    "namespace_id": namespace_id,
                    "type": namespace_type,
                    "questions": questions
                },
                headers={
                    "Authorization": "Bearer "+settings.LARAVEL_API_KEY
                }
            )