from typing import Tuple

from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from model_picker.llm_chooser import llm_chooser
from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    summary_template = """
        given the Linkedin information {information} about a person I want you to create:
        1. A short summary
        2. Two interesting facts about them
        3. A topic that may interest them
        4. 2 Creative Ice Breakers to open a conversation with them
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = llm_chooser()

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.invoke(input={"information": linkedin_data})["text"]
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    res = ice_break(name="Chen Goldberg")
    print(res)
