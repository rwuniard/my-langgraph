from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),

    ]
)

reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system", "You are a viral twitter influencer grading a tweet. Generate a critique and recommendation for the user's tweet."
        "Always provide detailed recommendations, including requests for length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages"),

])

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

generate_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm