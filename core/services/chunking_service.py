from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.settings import Settings

settings = Settings()


class ChunkingService:
    CHUNKING_FROM_FILE = 1
    CHUNKING_FROM_TEXT = 2

    def __init__(self):
        pass

    def chunkify_text(
            self,
            transcript_file = None,
            transcript = None,
            chunk_size = 1000,
            chunk_overlap = 100,
            chunking_mode = CHUNKING_FROM_FILE
    ):
        """
        Generates the snaps

        :return:
        """

        # Preprocess the text
        if chunking_mode == self.CHUNKING_FROM_FILE:
            loader = TextLoader(transcript_file)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = text_splitter.split_documents(documents)
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            docs = [Document(page_content=x) for x in text_splitter.split_text(transcript)]
        return docs