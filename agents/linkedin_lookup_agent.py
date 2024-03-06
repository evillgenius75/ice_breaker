from model_picker.llm_chooser import llm_chooser
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate


from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = llm_chooser()
    template = """given the full name {name_of_person} I want you to get me a link to their LinkedIn profile
    Your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for a linkedin profile page",
            func=get_profile_url,
            description="useful for when you need to get the LinkedIn Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url
