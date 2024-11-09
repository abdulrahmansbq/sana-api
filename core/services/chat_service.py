import chromadb
import torch
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from transformers import BertModel, BertTokenizer

from core.services.embedding_service import EmbeddingService
from core.settings import Settings

settings = Settings()


# Initialize BERT model and tokenizer
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")


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
            embedding_function=self.embedding_service.bert_model,
        )
        self.collection = chroma_client.get_collection("yt-" + namespace_id)

    # Get the prompt
    def get_prompt(self):
        """
        Responds to the chat message

        :return:
        """
        # Perform proximity search
        context, video_title = self.proximity_search(self.message)
        # Prepare the prompt
        prompt = self._prepare_prompt(context, video_title)
        return prompt

    def proximity_search(self, question: str, k: int = 3) -> str:
        """
        Perform proximity-based search using BERT embeddings.

        :param question: The question to search for
        :param k: Number of similar documents to retrieve
        :return: Combined context as a single string
        """
        # Encode the question using BERT
        input_ids = bert_tokenizer.encode(question, return_tensors="pt")

        # Obtain the embedding for the [CLS] token
        with torch.no_grad():
            output = bert_model(input_ids)[0]
            query_vectors = output[:, 0, :]  # Take the embedding of the [CLS] token

        # Query the Chroma collection
        query_result = self.collection.query(
            query_embeddings=query_vectors.squeeze().tolist(),
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        # Extract and combine document contents
        documents = list(reversed(query_result["documents"][0]))
        context = " \n ".join(documents)
        # get the metadatas and get the video_title
        metadatas = query_result["metadatas"][0]
        video_title = metadatas[0]["video_title"]

        return context, video_title

    # Prepare the prompt
    def _prepare_prompt(self, context, video_title):
        """
        Gets the message

        :param context: The context
        :return: The message
        """
        with open(settings.PROMPTS_PATH + "chat_prompt.txt", "r") as prompt_file:
            prompt = prompt_file.read()

        template = PromptTemplate.from_template(prompt)
        processed_prompt = template.format(
            context=context, question=self.message, lesson_title=video_title
        )
        return processed_prompt
