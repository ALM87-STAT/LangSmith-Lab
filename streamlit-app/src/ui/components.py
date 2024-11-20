# src/ui/components.py
import streamlit as st
from config.settings import Settings
from services.feedback_service import FeedbackService


class UserStoryUI:
    def __init__(self):
        self.feedback_service = FeedbackService()

    @staticmethod
    def initialize_session_state():
        if "generated_response" not in st.session_state:
            st.session_state.generated_response = None
        if "feedback_sent" not in st.session_state:
            st.session_state.feedback_sent = False

    @staticmethod
    def render_sidebar():
        st.sidebar.title("Contexto")
        context = st.sidebar.text_area(
            "Ingrese el contexto del proyecto:",
            value=st.session_state.get("context", ""),
            key="context_input",
        )

        with st.sidebar:
            st.markdown("## Ejemplo de Contexto" + "\n" + Settings.DEFAULT_CONTEXT)

        return context

    @staticmethod
    def render_requirements_form():
        with st.form("my_form"):
            requirements = st.text_area(
                "Ingrese los requisitos para generar la HU:",
                value=st.session_state.get("requirements", ""),
                placeholder=Settings.DEFAULT_REQUIREMENTS,
                key="requirements_input",
            )
            col1, col2 = st.columns([0.2, 0.8])

            with col1:
                submitted = st.form_submit_button("Generar")
            with col2:
                regenerate = st.form_submit_button("Generar de nuevo")
                st.session_state.feedback_sent = False

            return requirements, submitted, regenerate

    def render_feedback_buttons(self, run_id):
        if not st.session_state.feedback_sent:
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("👍 Útil"):
                    return self.feedback_service.send_feedback(run_id, 1)
            with col2:
                if st.button("👎 No es útil"):
                    return self.feedback_service.send_feedback(run_id, 0)
