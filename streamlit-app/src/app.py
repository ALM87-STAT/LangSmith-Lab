# app.py
import streamlit as st
from ui.components import UserStoryUI
from services.api_service import APIService


def main():
    # Set page title
    st.set_page_config(page_title="📝 Main Page")
    st.title("📝 Main Page")

    # Initialize services
    api_service = APIService()
    user_story_ui = UserStoryUI()

    # Initialize session state for response if it doesn't exist
    user_story_ui.initialize_session_state()

    # Nueva historia button
    if st.button("Nueva historia"):
        st.session_state.generated_response = None
        st.session_state.requirements_input = ""

    # Sidebar context
    context = user_story_ui.render_sidebar()

    # Requirements form
    requirements, submitted, regenerate = user_story_ui.render_requirements_form()

    # Generate response
    if submitted or regenerate:
        response_data = api_service.generate_user_story(context, requirements)
        if response_data:
            st.session_state.generated_response = response_data["response"]
            st.session_state.feedback = {"run_id": str(response_data["trace"])}

    # Display generated response
    if st.session_state.generated_response:
        st.markdown(st.session_state.generated_response)
        # Feedback buttons
        user_story_ui.render_feedback_buttons(st.session_state.feedback.get("run_id"))


if __name__ == "__main__":
    main()
