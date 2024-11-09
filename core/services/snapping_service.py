import json

import httpx
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from langchain_core.prompts import PromptTemplate

from core.settings import Settings

settings = Settings()


class SnappingService:
    def __init__(self):
        pass

    # Get the prompt
    def get_prompt(self, context):
        """
        Gets the message

        :param context: The context
        :return: The message
        """

        # Open the prompt file
        prompt_file = open(settings.PROMPTS_PATH + "snap_prompt.txt", "r")

        # Read the prompt file
        prompt = prompt_file.read()

        # Close the prompt file
        template = PromptTemplate.from_template(prompt)

        # Process the prompt
        processed_prompt = template.format(
            context=context,
            json_format='{{\n"sentences": ["summary sentence 1", "summary sentence 2", "summary sentence 3", ...]\n}}',
        )

        # Return the processed prompt
        return processed_prompt

    # Validate the JSON that was sent
    def validate_json(self, data):
        schema = {
            "type": "object",
            "properties": {
                "sentences": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,  # You can adjust the minimum number of items if needed
                }
            },
            "required": ["sentences"],
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

    # Send the snaps to the frontend
    def send_to_frontend(self, namespace_id, namespace_type, snaps):
        with httpx.Client(verify=False) as client:
            client.post(
                settings.LARAVEL_ENDPOINT + "/api/snaps",
                json={
                    "namespace_id": namespace_id,
                    "type": namespace_type,
                    "snaps": snaps,
                },
                headers={"Authorization": "Bearer " + settings.LARAVEL_API_KEY},
            )
