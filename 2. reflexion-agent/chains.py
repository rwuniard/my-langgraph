import datetime
import os
from dotenv import load_dotenv

load_dotenv()



from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser, PydanticToolsParser
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from schemas import AnswerQuestion, RevisedAnswer


# LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o")

# Parser
parser = JsonOutputToolsParser(return_id=True)
answerquestion_parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])
revisedanswer_parser_pydantic = PydanticToolsParser(tools=[RevisedAnswer])


# Actor prompt template
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher.
            Current time: {time}
            1. {first_instruction}
            2. Reflect and critique your answer. Be severe to maximize the quality of the answer.
            3. Recommend search queries to research information and improve the answer.
            
            IMPORTANT: Your response must include:
            - answer: Your detailed response
            - reflection: An object with 'missing' and 'superfluous' critiques 
            - search_queries: A list of search queries (NOT inside reflection)""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format.")
    ]
).partial(time=lambda: datetime.datetime.now().isoformat())

# First responder prompt template
first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detail ~250 words answer."
)


# Revisor prompt template
revise_instruction = """Revise your previous answer using the new information
        - You should use the previous critique to add important information to your answer.
            - You MUST include numerical citations in your revised answer to ensure accuracy.
            - Add a "References" section at the end of your answer (which doesn't count towards the word limit). In form of:
                - [1] https://example.com
                - [2] https://example.com
        - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words."""

revisor_prompt_template = actor_prompt_template.partial(
    first_instruction=revise_instruction
)

# First responder chain
first_responder_chain = (
    first_responder_prompt_template | 
    llm.with_structured_output(AnswerQuestion)
)

# Revisor chain
revisor_chain = (
    revisor_prompt_template | 
    llm.with_structured_output(RevisedAnswer)
)


if __name__ == "__main__":
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc problem domain."
        " list startups that do that and raised capital."
    )



    # First responder
    result = first_responder_chain.invoke({"messages": [human_message]})
    print("First Responder Result:")
    print("--------------------------------")
    print("Answer:", result[0].answer)
    print("--------------------------------")
    print("Search Queries:", result[0].search_queries)
    print("--------------------------------")
    print("Reflection:", result[0].reflection)





