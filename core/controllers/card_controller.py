# from langchain_core.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# import httpx

from core.settings import Settings

settings = Settings()

# PROMPT = """
# You are a video analyzing tool. I will give you a chunk of the transcription encapsulated in <context> tag to be aware of the context of the video.
# The context often contains textual mistakes so try hardly to understand.
# Your task is to explain the chunk in 2-3 sentences in each card.
# we need 2-3 cards comes in the same format given under JSON Format.
# You must not write anything other than the json object under json format.
# The cards must be in the same language as the context.
#
# <context>
#   {context}
# </context>
# """
#
# JSON_FORMAT = """
# JSON Format:
# {
#     "cards": [
#         "here is the first content",
#         "here is the second content",
#     ]
# }
# """


class CardController:
    def __init__(self, chunks, namespace_id):
        self.chunks = chunks
        self.namespace_id = namespace_id

    def generate(self):
        # for chunk in self.chunks:
        #     self._generate_card(chunk)
        pass

    def _generate_card(self, chunk):
        # print(chunk)
        # print("1- Loading LLM")
        # llm = ChatOpenAI(model_name=settings.OPENAI_CHAT_MODEL, temperature=1)
        # print("2- Loading QA Chain")
        # print("6- Returning answer")
        # answer_prompt = PromptTemplate.from_template(PROMPT)
        # response = llm.invoke(input=(answer_prompt.format_prompt(context=chunk.page_content).to_string()+JSON_FORMAT))
        # print(response)
        # with httpx.Client() as client:
        #     response = client.post(
        #         settings.LARAVEL_ENDPOINT+"videos/"+self.namespace_id+"/summary",
        #         json={
        #             "content": response.content,
        #         },
        #     )
        # return {"status": "Success", "message": response}
        pass