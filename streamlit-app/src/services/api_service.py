# src/services/api_service.py
import opik
from opik import Opik
import requests
import streamlit as st
from config.settings import Settings
from services.feedback_service import FeedbackService
from utils.experiment_utils import generate_experiment_name


class APIService:
    def __init__(self):
        self.settings = Settings()
        self.feedback_service = FeedbackService()

    def generate_user_story(self, context, requirements):
        try:
            with st.spinner("Generando historia de usuario..."):
                response = requests.post(
                    self.settings.API_URL,
                    json={
                        "input": {"contexto": context, "requisitos": requirements},
                        "config": {},
                        "kwargs": {},
                    },
                )
                if response.status_code == 200:
                    response = response.json()["output"].replace("\n", "  \n  ")
                    trace = self.feedback_service.create_trace(
                        generate_experiment_name(), context, requirements, response
                    )
                    return {"response": response, "trace": str(trace.id)}
                else:
                    st.error("Error al comunicarse con la API")
                    return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
