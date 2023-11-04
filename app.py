import os
from embedchain import App
import streamlit as st
import base64
from api import getKey

api_key = getKey()
os.environ['OPENAI_API_KEY'] = api_key
app = App()


st.title("Study Buddy Bot...")

def predict(template, prompt, chat_history):
    response = app.query(template)
    chat_history.append((prompt, response))
    return "", chat_history

app.add('./data/How_linux_works.pdf', data_type='pdf_file')
# app.add('./data/just_for_fun_linus_books.pdf', data_type='pdf_file')

prompt = st.text_input("Enter You Prompt here...")

template = f"""
Act as a Linux expert. You are good at creating best curriculum, teaching students according to their weekness by developing
basic questions about the topic. 

PROMPT: {prompt}
"""

chat_history = []

if st.button("Submit"):
    if prompt:
        _, chat_history = predict(template, prompt, chat_history)

for usr_prompt, response in chat_history:
    st.write(f"You: {usr_prompt}")
    st.write("Chatbot:", response)

if st.button("Clear Chat History"):
    chat_history = []

# if prompt:
#     response = app.query(template)
#     st.write(response)
