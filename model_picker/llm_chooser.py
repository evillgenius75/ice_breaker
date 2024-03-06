import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


def llm_chooser() -> ChatOpenAI | ChatGoogleGenerativeAI:
    if os.environ.get("LLM") == "OPENAI":
        llm_choice = ChatOpenAI(model_name="gpt-3.5-turbo")
    elif os.environ.get("LLM") == "GOOGLE" or os.environ.get("LLM") is None:
        llm_choice = ChatGoogleGenerativeAI(model="gemini-pro")
    else:
        raise ValueError("Invalid LLM")
    return llm_choice
