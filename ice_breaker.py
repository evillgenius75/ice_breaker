from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://gist.githubusercontent.com/evillgenius75/a4afe97f0f8a233b5ee738167a5fefa5/raw"
                             "/7028b8eef25dce9887440d21dc743afb7466af1d/linkedin.json"
    )

    print(chain.invoke(input={"information": linkedin_data})["text"])
