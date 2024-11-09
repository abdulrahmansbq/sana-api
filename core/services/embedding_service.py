import random
import string
from uuid import uuid4

import chromadb
import torch
from transformers import BertModel, BertTokenizer

from core.services.chunking_service import ChunkingService
from core.settings import Settings

settings = Settings()


class EmbeddingService:
    # Initialize the EmbeddingService with BERT
    def __init__(self):
        # Load BERT model and tokenizer
        self.bert_model = BertModel.from_pretrained("bert-base-uncased")
        self.bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # Generate embeddings
    def generate_embeddings(self, texts, video_title):
        vector_embeddings = []
        vector_documents = []
        vector_metadatas = []
        vector_ids = []

        # Generate embeddings for each text
        for i, text in enumerate(texts):
            # Encode the text using the BERT tokenizer
            input_ids = self.bert_tokenizer.encode(
                text.page_content, return_tensors="pt"
            )

            with torch.no_grad():
                output = self.bert_model(input_ids)[0]
                embedding = output[:, 0, :]  # Take the embedding of the [CLS] token

            # Append the embedding, document, and metadata to the respective lists
            vector_embeddings.append(embedding.squeeze().tolist())
            vector_documents.append(text.page_content)
            metadata = {
                "chunk_number": i,
                "text_length": len(text.page_content),
                "video_title": video_title,
            }
            vector_metadatas.append(metadata)
            random_string = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            id = "{}-{}".format(i, random_string)
            vector_ids.append(id)
            print("Document {} has been embedded.".format(i))

        # Return the embeddings, documents, metadatas, and ids
        return vector_embeddings, vector_documents, vector_metadatas, vector_ids

    # Embed the transcript
    def embed_transcript(
        self, text_file: str, chrome_client, namespace_id, video_title
    ):
        """
        Embeds the text in the database
        """
        # Process and chunk the transcript file
        docs = ChunkingService().chunkify_text(
            transcript_file=text_file, chunk_size=400, chunk_overlap=100
        )

        # Generate embeddings
        vector_embeddings, vector_documents, vector_metadatas, vector_ids = (
            self.generate_embeddings(docs, video_title)
        )

        # Get or create the collection in ChromaDB
        collection = chrome_client.get_or_create_collection(name=namespace_id)

        # Add the vectors, documents, and metadata to the ChromaDB collection
        collection.add(
            embeddings=vector_embeddings,
            documents=vector_documents,
            metadatas=vector_metadatas,
            ids=vector_ids,
        )

    # Embed a query
    def embed_query(self, query: str):
        """
        Embeds a query
        """
        # Encode the query using the BERT tokenizer
        input_ids = self.bert_tokenizer.encode(query, return_tensors="pt")
        # Obtain the embedding for the [CLS] token
        with torch.no_grad():
            output = self.bert_model(input_ids)[0]
            embedding = output[:, 0, :]  # Use [CLS] token embedding

        # Return the embedding
        return embedding.squeeze().tolist()
