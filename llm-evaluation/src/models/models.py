from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI

from src.config.config_loader import ConfigLoader


config = ConfigLoader().get_config


class ChatModels:
    def __init__(self, config=config):
        self.config = config

    def _select_model(self, model_config) -> object:
        if model_config.provider == "vertex_ai":
            vertex_ai = ChatVertexAI(**model_config.parameters)
            return vertex_ai
        elif model_config.provider == "openai":
            openai = ChatOpenAI(**model_config.parameters)
            return openai

    @property
    def app_llm(self) -> object:
        return self._select_model(self.config.models.application)

    @property
    def eval_llm(self) -> object:
        return self._select_model(self.config.models.evaluator)
