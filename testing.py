import streamlit as st
import pandas as pd

from langchain_community.chat_message_histories import SQLChatMessageHistory

from langchain_google_genai import ChatGoogleGenerativeAI
import os


# Access the API key
key = st.secrets["GOOGLE_API_KEY"]


chat_model = ChatGoogleGenerativeAI(api_key = key, model = 'gemini-1.5-flash')

# Retrieves the history for a particular session using session id
def get_messages_history_from_db(session_id):
    chat_history = SQLChatMessageHistory(session_id = session_id, connection = st.secrets["DB_CONNECTION_STRING"])
    return chat_history

# Creating a chat template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
chat_template = ChatPromptTemplate.from_messages([('system', '''You name is Freddy and You are known to be a very helpful, interactive 
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
                              biased remarks.'''),
                                                  MessagesPlaceholder(variable_name = 'history'),
                                                  ('human', '{human_input}')])

# creating a chain
chain = chat_template | chat_model

#bringing the memory and the chain (pipeline) together
from langchain_core.runnables import RunnableWithMessageHistory
conversational_chain = RunnableWithMessageHistory(chain,
                                                  get_messages_history_from_db,
                                                  history_messages_key = 'history',
                                                  input_messages_key = 'human_input')

#configuring the session id and invoking the chain

st.title('Freddy the AI Bot')
user_id = st.text_input("Please tell me your name to start the conversation:")
if user_id:
    config = {'configurable' : {'session_id' : user_id}}


    st.chat_message('assistant').write(f"Hi {user_id}! How may I help you?")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).write(msg['content'])

    user_input = st.chat_input()


    if user_input:

        input_prompt = {'human_input' : user_input}

        st.chat_message('user').write(user_input)
        
        response = conversational_chain.invoke(input_prompt, config = config)
    
        st.chat_message('assistant').write(response.content)

        st.session_state['messages'].append({'role' : 'user', 'content' : user_input})

        st.session_state['messages'].append({'role' : 'assistant', 'content' : response.content})


