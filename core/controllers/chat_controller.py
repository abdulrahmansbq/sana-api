from chromadb.errors import InvalidCollectionException
import chromadb
from langchain_ibm import WatsonxLLM
from core.services.chat_service import ChatService
from core.settings import Settings

settings = Settings()

class ChatController:
    def __init__(self, namespace_id, message):
        self.namespace = namespace_id
        self.message = message
        self.chroma_client = chromadb.PersistentClient(path=settings.STORAGE_PATH + "chroma/")
        self.chat_model = WatsonxLLM(
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

    async def chat(self):
        try:
            self.chroma_client.get_collection("yt-"+self.namespace)
        except InvalidCollectionException:
            return {"status": "Error", "message": "Namespace does not exist"}

        prompt = ChatService(
            chroma_client=self.chroma_client,
            namespace_id=self.namespace,
            message=self.message
        ).get_prompt()

        answer = self.chat_model.invoke(prompt)

        return {"status": "Success", "message": answer}
