import asyncio  # Add this import for async operations

# Existing imports
import tempfile
from uuid import uuid4

import chromadb
from chromadb import PersistentClient
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
from transformers import BertModel, BertTokenizer

from core.controllers.exam_controller import ExamController
from core.controllers.snap_controller import SnapController
from core.services.chunking_service import ChunkingService
from core.services.embedding_service import EmbeddingService
from core.settings import Settings


async def _generate_snaps(namespace_id, transcript, namespace_type):
    # Generate snaps using the SnapController
    await SnapController(namespace_id, transcript, namespace_type).generate()


async def _generate_exam(namespace_id, transcript, namespace_type):
    # Generate exam using the ExamController
    await ExamController(namespace_id, namespace_type, transcript).generate()


async def main():
    # Load settings
    settings = Settings()

    # Define your persistent Chroma client with a specified storage path
    chroma_client = chromadb.PersistentClient(path=settings.STORAGE_PATH + "chroma/")

    # Path to the transcript file
    transcript_file = "lesson2.txt"
    namespace_id = transcript_file
    video_title = "Lesson 2 Video Title"  # Add the actual title of the video

    # Initialize the EmbeddingService with BERT
    embedding_service = EmbeddingService()

    # Read and process the transcript file
    with open(settings.STORAGE_PATH + transcript_file, "r") as opened_transcript:
        saved_transcript = opened_transcript.read()

    # Check if the namespace already exists
    try:
        collection = chroma_client.get_collection(namespace_id)
        print(f"Error: Namespace '{namespace_id}' already exists.")
    except chromadb.errors.InvalidCollectionException:
        print("Namespace does not exist; proceeding with embedding.")

        # Save transcript content to a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8"
        ) as temp_file:
            temp_file.write(saved_transcript)
            temp_file_path = temp_file.name

        # Chunk the text using the path of the temporary file
        docs = ChunkingService().chunkify_text(
            transcript_file=temp_file_path, chunk_size=400, chunk_overlap=100
        )

        # Generate embeddings using the updated EmbeddingService
        vector_embeddings, vector_documents, vector_metadatas, vector_ids = (
            embedding_service.generate_embeddings(texts=docs, video_title=video_title)
        )

        # Get or create the collection in ChromaDB
        collection = chroma_client.get_or_create_collection(name=namespace_id)

        # Add the vectors, documents, and metadata to the ChromaDB collection
        collection.add(
            embeddings=vector_embeddings,
            documents=vector_documents,
            metadatas=vector_metadatas,
            ids=vector_ids,
        )

        # Await _generate_snaps in the asynchronous main function
        await _generate_snaps(namespace_id, saved_transcript, "lesson")
        await _generate_exam(namespace_id, saved_transcript, "lesson")

        print("Transcript embedding completed with namespace ID:", namespace_id)


# Run the main function in an asynchronous event loop
asyncio.run(main())
