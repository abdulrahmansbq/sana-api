from uuid import uuid4
import chromadb
from chromadb import PersistentClient
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from core.services.chunking_service import ChunkingService
from core.services.embedding_service import EmbeddingService
from core.settings import Settings
import tempfile

# Load settings
settings = Settings()

# Define your persistent Chroma client with a specified storage path
chroma_client = PersistentClient(path=settings.STORAGE_PATH + "chroma/")

# Path to the transcript file
transcript_file = "lesson1.txt"

namespace_id = transcript_file
embeddings_model = HuggingFaceEmbeddings(model_name='sentence-transformers/multi-qa-mpnet-base-dot-v1',
                                         model_kwargs={'device': settings.WHISPER_DEVICE})


with open(settings.STORAGE_PATH + transcript_file, "r") as opened_transcript:
    saved_transcript = opened_transcript.read()

# Check if the namespace already exists
try:
    collection = chroma_client.get_collection(namespace_id)
    print(f"Error: Namespace '{namespace_id}' already exists.")
except InvalidCollectionException:
    print("Namespace does not exist; proceeding with embedding.")

    # Save transcript content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(saved_transcript)
        temp_file_path = temp_file.name

    # Chunk the text using the path of the temporary file
    docs = ChunkingService().chunkify_text(transcript_file=temp_file_path, chunk_size=450, chunk_overlap=100)

    # Generate unique IDs for each document chunk
    uuids = [str(uuid4()) for _ in range(len(docs))]

    # Initialize the Chroma client for embedding
    chroma_client = Chroma(
        client=chroma_client,
        collection_name=namespace_id,
        embedding_function=embeddings_model,
    )

    # Add documents to Chroma
    chroma_client.add_documents(documents=docs, ids=uuids)

    print("Transcript embedding completed with namespace ID:", namespace_id)
