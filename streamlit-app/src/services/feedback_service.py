import opik
from opik import Opik
import streamlit as st
from config.settings import Settings


class FeedbackService:
    def __init__(self):
        opik.configure(use_local=True, url=Settings.OPIK_LOCAL_URL)
        self.client = Opik()

    def create_trace(self, name, context, requirements, response):
        return self.client.trace(
            name=name,
            input={"contexto": context, "input": requirements},
            output={"output": response},
        )

    def send_feedback(self, trace_id, score):
        try:
            self.client.log_traces_feedback_scores(
                scores=[
                    {
                        "id": trace_id,
                        "name": "user_feedback",
                        "value": score,
                    }
                ]
            )
            st.success("¡Gracias por tu feedback!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
