from langchain_core.output_parsers import StrOutputParser
from src.core.models import ChatModels
from src.core.templates import PromptTemplates


class CreateChain:
    def __init__(self):
        self.str_parser = StrOutputParser()
        self.llm = ChatModels().get_model

    @property
    def create_chain(self) -> object:
        return PromptTemplates.app_prompt_template | self.llm | self.str_parser
