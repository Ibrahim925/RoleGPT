from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv


def main():
    st.set_page_config(page_title="RoleGPT", page_icon="👽")
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        system_message = st.text_input(label="GPT Role")
        user_prompt = st.text_input(label="Send a message...")

        if system_message:
            if not any(
                isinstance(message, SystemMessage)
                for message in st.session_state.messages
            ):
                st.session_state.messages.append(SystemMessage(content=system_message))

        if user_prompt:
            st.session_state.messages.append(HumanMessage(content=user_prompt))

            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)

            st.session_state.messages.append(AIMessage(content=response.content))

    for i, chat_message in enumerate(st.session_state.messages):
        if isinstance(chat_message, HumanMessage):
            message(chat_message.content, is_user=True, key=f"User #{i}")
        elif isinstance(chat_message, AIMessage):
            message(chat_message.content, is_user=False, key=f"AI #{i}")


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    main()
