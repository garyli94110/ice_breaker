from click import prompt
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_community.chat_models.litellm_router import model_extra_key_name
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub

from dotenv import load_dotenv
import os

from numpy.f2py.crackfortran import verbose

from tools.tools import get_profile_url_tavily


def lookup(name: str) ->  str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    )
    template = """
        given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
        your answer should contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the linkedin page URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm, tools=tools_for_agent, prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True
    )
    result = agent_executor.invoke(
        input = { "input": prompt_template.format_prompt(name_of_person=name)}
    )
    return result["output"]

if __name__ == "__main__":
    linkedin_url=lookup(name="Eden Marco")
    print( linkedin_url   )