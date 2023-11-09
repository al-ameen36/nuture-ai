import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.vectorstores import Vectara

load_dotenv()

# Constants
CUSTOMER_ID = os.getenv("CUSTOMER_ID")
VECTARA_API_KEY = os.getenv("VECTARA_API_KEY")
CORPUS_ID = int(os.getenv("CORPUS_ID", 0))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def initialize_vectara():
    vectara = Vectara(
        vectara_customer_id=CUSTOMER_ID,
        vectara_corpus_id=CORPUS_ID,
        vectara_api_key=VECTARA_API_KEY,
    )
    return vectara


vectara_client = initialize_vectara()


def get_knowledge_content(vectara, query, threshold=0.5):
    found_docs = vectara.similarity_search_with_score(
        query,
        score_threshold=threshold,
    )
    knowledge_content = ""
    for number, (score, doc) in enumerate(found_docs):
        knowledge_content += (
            f"Document {number}: {found_docs[number][0].page_content}\n"
        )
    return knowledge_content


def inform_user(msg):
    with st.chat_message("assistant"):
        st.write(msg)


with st.sidebar:
    st.header("Options")
    name = st.text_input("Your Name", "kulu")
    age = st.number_input("Your Age", value=21, min_value=13, max_value=60)
    trimester = st.selectbox(
        "What stage is your pregnancy?",
        ["First trimester", "Second trimester", "Third trimester"],
    )

    st.header("Reminders and tips")
    phone = st.text_input(
        "Your Phone Number", disabled=True, placeholder="Currently unavailable"
    )
    reminders = st.checkbox("Receive reminders and tips", disabled=True)


prompt = PromptTemplate.from_template(
    """You are a professional and friendly Maternal Health adviser and you are helping an expecting mother. She is asking you for advice on a maternal health issues. Your answer should be in markdown notation/syntax. Answer her directly in detail (make sure your answer is relevant to her trimester: {trimester}, her age: {age}, her name: {name}) and nothing else. your answer must not be more than 300 characters. This is the issue: {issue}
    Answer her question with the following information: {knowledge}
    """
)
# include the reg infoin every query

regFeedback = PromptTemplate.from_template(
    """You are a professional and caring Maternal Health Consultant and you can help with maternal health issues. An expecting mother just registered for your service. You can give good comforting feedback to her (summarize your answer not more than 400 characters). Your answer should be in markdown notation/syntax. There registered info {reg_info}
    """
)

runnable = (
    prompt
    | ChatOpenAI(
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        openai_api_key=OPENAI_API_KEY,
    )
    | StrOutputParser()
)
feedback = (
    regFeedback
    | ChatOpenAI(
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        openai_api_key=OPENAI_API_KEY,
    )
    | StrOutputParser()
)

# Main Streamlit App
st.title("Nuture AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if len(st.session_state.messages) == 0:
    # initial bot messages
    welcome_msgs = [
        f"Hello {name}. I am pleased to be your dedicated Maternal Health Consultant and I am here to support you throughout your pregnancy journey. Rest assured that your well-being and the health of your baby are my top priorities, ensuring a safe and enjoyable pregnancy experience for you and your baby.",
        "Please feel free to reach out to me at any time with your questions, concerns, or any updates regarding your pregnancy/baby.",
    ]
    for msg in welcome_msgs:
        inform_user(msg)
        time.sleep(0.5)
        st.session_state.messages.append({"role": "assistant", "content": msg})


if user_input := st.chat_input("Enter your question:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("Thinking...") as status:
        knowledge_content = get_knowledge_content(vectara_client, user_input)
        print("__________________ Start of knowledge content __________________")
        print(knowledge_content)

        response = runnable.invoke(
            {
                "knowledge": knowledge_content,
                "issue": user_input,
                "trimester": trimester,
                "name": {name},
                "age": age,
            }
        )
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
