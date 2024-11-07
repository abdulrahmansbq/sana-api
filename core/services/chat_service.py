import chromadb
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from core.services.embedding_service import EmbeddingService
from core.settings import Settings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


settings = Settings()

class ChatService:
    def __init__(
            self,
            chroma_client: chromadb,
            namespace_id: str,
            message: str,
    ):
        self.namespace_id = namespace_id
        self.message = message
        self.embedding_service = EmbeddingService()
        self.chroma_client = Chroma(
            client=chroma_client,
            collection_name=namespace_id,
            embedding_function=self.embedding_service.embeddings_model,
        )

    def get_prompt(self):
        """
        Responds to the chat message

        :return:
        """


        embedded_question = self.embedding_service.embed_query(self.message)

        context = self._get_context(embedded_question)

        prompt = self._prepare_prompt(context)

        return prompt

    def _get_context(self, embedded_question):
        """
        Gets the combined context from the top 3 similar results.

        :param embedded_question: The embedded question vector
        :return: Combined context as a single string
        """

        results = self.chroma_client.similarity_search_by_vector(embedded_question, k=1)

        context = " \n ".join(res.page_content for res in results)

        return context

    def _prepare_prompt(self, context):
        """
        Gets the message

        :param context: The context
        :return: The message
        """

        prompt_file = open(settings.PROMPTS_PATH + "chat_prompt.txt", "r")

        prompt = prompt_file.read()

        template = PromptTemplate.from_template(prompt)

        processed_prompt = template.format(context=context,question=self.message)

        return processed_prompt