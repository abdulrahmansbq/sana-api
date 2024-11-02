from uuid import uuid4

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from core.services.chunking_service import ChunkingService
from core.settings import Settings

settings = Settings()


class EmbeddingService:
    def __init__(
            self,
    ):
        self.embeddings_model = HuggingFaceEmbeddings(model_name='sentence-transformers/multi-qa-mpnet-base-dot-v1',
                                                      model_kwargs={'device': settings.WHISPER_DEVICE})

    def embed_transcript(
            self,
            text_file: str,
            chrome_client: chromadb,
            namespace_id
    ):
        """
        Embeds the text in the database

        :return:
        """

        chroma_client = Chroma(
            client=chrome_client,
            collection_name=namespace_id,
            embedding_function=self.embeddings_model,
        )

        docs = ChunkingService().chunkify_text(transcript_file=text_file, chunk_size=400, chunk_overlap=100)
        uuids = [str(uuid4()) for _ in range(len(docs))]

        chroma_client.add_documents(documents=docs, ids=uuids)

    def embed_query(self, query: str):
        """
        Embeds the query

        :return:
        """
        return self.embeddings_model.embed_query(query)