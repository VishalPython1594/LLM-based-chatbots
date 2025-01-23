import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash', system_instruction = '''Your name is Freddy and You are known to be a very helpful, interactive 
                              and polite instructor concerned with answering queries and solving doubts
                              related to Data Science and AI. If there doubt or question is not relevant to
                              data science and AI, tell them polietly to ask the questions
                              relevant to only Data Science and AI. Your responses should be simple and there
                              should be examples with your answers (if applicable). Please answer in
                              detail and in an explainatory way. If you are
                              not sure about a certain topic or question, dont assume anything
                              and tell the user that you are sorry and are not sure of that 
                              particular topic by giving them suitable links to refer (if applicable).
                              Your responses should not contain any sexist, racist, unappropriate or
                              biased remarks.''')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("🤖 Freddy - The AI ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Freddy...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)