from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate

from src.models.prompts import (
    EVALUATION_PROMPT,
    APP_SYSTEM_PROMPT,
    APP_USER_PROMPT,
)


class PromptTemplates:
    evaluation_prompt_template = PromptTemplate(
        input_variables=["experto", "asistente"],
        template=EVALUATION_PROMPT,
    )

    app_prompt_template = ChatPromptTemplate.from_messages(
        [("system", APP_SYSTEM_PROMPT), ("user", APP_USER_PROMPT)]
    )
