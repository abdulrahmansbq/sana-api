from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.formatters.snap_formatter import SnapFormatter
from core.services.embedding_service import EmbeddingService
from core.settings import Settings

settings = Settings()


class SnappingService:
    def __init__(self):
        pass

    def chunkify_text(self, transcript):
        """
        Generates the snaps

        :return:
        """

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = [Document(page_content=x) for x in text_splitter.split_text(transcript)]

        return docs



    def get_prompt(self, context):
        """
        Gets the message

        :param context: The context
        :return: The message
        """

        prompt_file = open(settings.PROMPTS_PATH + "snap_prompt.txt", "r")

        prompt = prompt_file.read()

        template = PromptTemplate.from_template(prompt)

        parser = JsonOutputParser(pydantic_object=SnapFormatter)

        processed_prompt = template.format(context=context,json_format='{{\n"sentences": ["summary sentence 1", "summary sentence 2", "summary sentence 3", ...]\n}}')

        print(processed_prompt)

        return processed_prompt