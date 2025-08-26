from dotenv import load_dotenv
from typing import List, TypedDict, Optional

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import START, END, StateGraph

from chains import first_responder_chain, revisor_chain
from tool_executor import run_queries
from schemas import AnswerQuestion, RevisedAnswer

MAX_ITERATIONS = 2

# Define the state schema
class GraphState(TypedDict):
    question: str
    current_answer: Optional[AnswerQuestion]
    revised_answer: Optional[RevisedAnswer]
    search_results: List[dict]  # Not optional - will be empty list initially
    iterations: int

def draft_node(state: GraphState) -> GraphState:
    """Generate initial response with reflection and search queries."""
    print("🔄 Executing draft_node...")
    # Create a human message for the chain
    human_message = HumanMessage(content=state["question"])
    
    # Get the response from the chain
    answer_obj = first_responder_chain.invoke({"messages": [human_message]})
    print("✓ Draft completed")
    
    return {
        **state,
        "current_answer": answer_obj,
        "iterations": state.get("iterations", 0)
    }

def execute_tools_node(state: GraphState) -> GraphState:
    """Execute search queries from the current answer."""
    print("🔄 Executing execute_tools_node...")
    if state["current_answer"] and state["current_answer"].search_queries:
        print(f"Running {len(state['current_answer'].search_queries)} search queries...")
        search_results = run_queries(state["current_answer"].search_queries)
        print("✓ Search completed")
        return {
            **state,
            "search_results": search_results
        }
    print("✓ No search queries to execute")
    return state

def revise_node(state: GraphState) -> GraphState:
    """Revise the response using search results."""
    print("🔄 Executing revise_node...")
    # Create messages for the revisor chain, including previous answer and search results
    human_message = HumanMessage(content=state["question"])
    
    messages = [human_message]
    
    # Add the current answer for context
    if state["current_answer"]:
        current_answer_context = f"Previous answer: {state['current_answer'].answer}"
        messages.append(HumanMessage(content=current_answer_context))
    
    # Add search results context if available
    if state["search_results"]:
        search_context = f"Additional research information: {state['search_results']}"
        messages.append(HumanMessage(content=search_context))
    
    # Get the revised response from the chain
    revised_obj = revisor_chain.invoke({"messages": messages})
    print("✓ Revision completed")
    
    return {
        **state,
        "revised_answer": revised_obj,
        "iterations": state.get("iterations", 0) + 1
    }

# Create the StateGraph
builder = StateGraph(GraphState)
builder.add_node("draft", draft_node)
builder.add_node("execute_tools", execute_tools_node)
builder.add_node("revise", revise_node)
builder.add_edge(START, "draft")
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")


def should_continue(state: GraphState) -> str:
    """Decide whether to continue or end the process."""
    iterations = state.get("iterations", 0)
    print(f"🔍 Checking iterations: {iterations}/{MAX_ITERATIONS}")
    if iterations >= MAX_ITERATIONS:
        print("📋 Reached max iterations, ending")
        return END
    else:
        print("🔄 Continuing to execute_tools")
        return "execute_tools"

builder.add_conditional_edges(
    "revise",
    should_continue,
    {
        END: END,
        "execute_tools": "execute_tools",
    },
)


builder.set_entry_point("draft")


def main():
    graph = builder.compile()

    # print("--------------------------------")
    # graph.get_graph().draw_mermaid_png(output_file_path="diagram.png")
    # print("--------------------------------")
    
    # Create initial state
    initial_state = {
        "question": "Write about AI-Powered SOC / autonomous soc problem domain. list startups that do that and raised capital.",
        "current_answer": None,
        "revised_answer": None,
        "search_results": [],  # Empty list initially, not None
        "iterations": 0
    }
    
    result = graph.invoke(initial_state)
    
    print("=== DRAFT ANSWER ===")
    if result["current_answer"]:
        print(f"Answer: {result['current_answer'].answer}")
        print(f"Search Queries: {result['current_answer'].search_queries}")
        print(f"Reflection: {result['current_answer'].reflection}")
    
    print("\n=== REVISED ANSWER ===")
    if result["revised_answer"]:
        print(f"Answer: {result['revised_answer'].answer}")
        print(f"References: {result['revised_answer'].references}")
    
    print(f"\nIterations: {result['iterations']}")


if __name__ == "__main__":
    main()