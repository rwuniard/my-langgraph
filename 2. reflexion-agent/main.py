from dotenv import load_dotenv
from typing import List

load_dotenv()

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import START, END, MessageGraph
from langgraph.prebuilt import ToolNode

from chains import actor_prompt_template, revisor_prompt_template, llm, first_responder_chain, revisor_chain
from tool_executor import execute_tools

MAX_ITERATIONS = 2

builder = MessageGraph()
builder.add_node("draft", first_responder_chain)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor_chain)
builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")
builder.add_edge("revise", END)


def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits >= MAX_ITERATIONS:
        return END
    else:
        return "execute_tools"

builder.add_conditional_edges(
    "revise",
    event_loop,
    {
        END: END,
        "execute_tools": "execute_tools",
    },
)

builder.set_entry_point("draft")


def main():
    graph = builder.compile()

    print("--------------------------------")
    print(graph.get_graph().draw_mermaid())
    print("--------------------------------")
    # graph.invoke({"messages": [HumanMessage(content="Write about AI-Powered SOC / autonomous soc problem domain."
    #     " list startups that do that and raised capital.")]})


if __name__ == "__main__":
    main()