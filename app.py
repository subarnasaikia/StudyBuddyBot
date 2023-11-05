import os
from embedchain import App
import streamlit as st
import base64
from api import getKey


def predict(template, prompt, chat_history):
    response = app.query(template)
    chat_history.append((prompt, response))
    return "", chat_history

api_key = getKey()
os.environ['OPENAI_API_KEY'] = api_key
app = App()


if not os.path.exists("data"):
    os.makedirs("data")

st.title("Study Buddy Bot...")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    pdf_contents = pdf_file.read()
    pdf_b64 = base64.b64encode(pdf_contents).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="500" height="800"></iframe>'
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)


    file_path = os.path.join("data", pdf_file.name)
    with open(file_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    app.add(file_path,data_type="pdf_file")

    prompt = st.text_input("Enter your query:")

    template = f"""
    You are the expert in the given. Using the given data and your trained knowledge give us the appropriate answers. You are good at creating best curriculum, teaching students according to their weekness by developing
    basic questions about the topic. 

    PROMPT: {prompt}
    """

    chat_history = []

    if prompt:
        with st.spinner("Generating..."):
            _, chat_history = predict(template, prompt, chat_history)

        for usr_prompt, response in chat_history:
            st.write(f"You: {usr_prompt}")
            st.write("Chatbot:", response)
