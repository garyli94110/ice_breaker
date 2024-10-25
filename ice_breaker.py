from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

from agents.linkedin_lookup_agent import lookup
from third_parties.linkedin import scrape_linkedin_profile

information = """
Version 2.1.10 was released on 10/09/2024 5:00pm by garyl553.  The release note contains these commits:
commit 21323: initial copy
commit 32453: update
commit 53432: udpate2
"""

def ice_break_with(name: str) -> str:
    linked_username = lookup(name=name)
    linkedin_data = scrape_linkedin_profile(lin)
    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them 
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | StrOutputParser()

    linkedin_data = scrape_linkedin_profile()

    response = chain.invoke(input={"information": linkedin_data})
    print(response)

if __name__ == "__main__":
    load_dotenv()
    ice_break_with()
