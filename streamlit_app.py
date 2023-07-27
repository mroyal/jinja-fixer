from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import jinja2
import openai
import streamlit as st
from langchain.schema import SystemMessage, HumanMessage

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Jinja Demo")
st.caption("This is a demo app to correct Jinja errors")
jinja_in = st.text_area("Jinja Input", value="Hello {{ contact2.first_name }}")

template = jinja2.Template(jinja_in)
try:
    content = template.render(contact={"first_name": "Vincent"})

    st.write("Jinja input:")
    st.code(jinja_in, language="jinja2")

    st.write("Content:")
    st.code(content, language="html")
except Exception as e:
    content = "Oops! There was an error"

    llm = ChatOpenAI(model="gpt-3.5-turbo")
    messages = [
        SystemMessage(
            content="You are a Jinja expert. Please fix this broken Jinja. The possible variables are: contact.first_name, contact.last_name, contact.email."),
        HumanMessage(content=f"Jinja: {jinja_in}\nError: {e}\nCorrected Jinja:"),
    ]
    response = llm(messages)

    st.write("Jinja input:")
    st.code(jinja_in, language="jinja2")

    st.write("Corrected Jinja:")
    st.code(response.content, language="jinja2")
