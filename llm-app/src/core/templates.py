from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

from src.core.prompts import SYSTEM_PROMPT, USER_PROMPT


class PromptTemplates:
    app_prompt_template = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("user", USER_PROMPT)]
    )
