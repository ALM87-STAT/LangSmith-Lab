from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI

from config.config_loader import ConfigLoader


config = ConfigLoader().get_config


class ChatModels:
    def __init__(self, config=config):
        self.config = config

    @property
    def get_model(self) -> object:
        if self.config.models.application.provider == "vertex_ai":
            vertex_ai = ChatVertexAI(**self.config.models.application.parameters)
            return vertex_ai
        elif self.config.models.application.provider == "openai":
            openai = ChatOpenAI(**self.config.models.application.parameters)
            return openai
