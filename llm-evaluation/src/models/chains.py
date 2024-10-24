from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from evaluation.templates import PromptTemplates
from models.models import ChatModels


class CreateChain:
    def __init__(self):
        self.json_parser = JsonOutputParser()
        self.str_parser = StrOutputParser()
        self.prompt_templates = PromptTemplates()
        self.models = ChatModels()

    def _create_chain(self, prompt_template, llm, parser):
        return prompt_template | llm | parser

    @property
    def app_chain(self) -> object:
        return self._create_chain(
            self.prompt_templates.app_prompt_template,
            self.models.app_llm,
            self.str_parser,
        )

    @property
    def eval_chain(self) -> object:
        return self._create_chain(
            self.prompt_templates.evaluation_prompt_template,
            self.models.eval_llm,
            self.json_parser,
        )
