from typing import List, Sequence, TypedDict


from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph, StateGraph
from chains import generate_chain, reflection_chain


class GraphState(TypedDict):
    messages: List[BaseMessage]



###############################################
#
#                     ----------> __end__
#                     |
#   __start__ --> Generate --> reflect
#                     ^           |
#                     |           |
#                      -----------
###############################################



REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: GraphState) -> GraphState:
    print("(Generation node", state["messages"])
    result = generate_chain.invoke({"messages": state["messages"]})
    return {"messages": state["messages"] + [result]}


def reflection_node(state: GraphState) -> GraphState:
    print("Reflection node", state["messages"])
    res = reflection_chain.invoke({"messages": state["messages"]})
    print("Reflection result", res)
    return {"messages": state["messages"] + [HumanMessage(content=res.content)]}
    
# builder = MessageGraph()
builder = StateGraph(GraphState)
# Adding the nodes to the graph
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
# Define that the starting point is Generate node.
builder.set_entry_point(GENERATE)

def should_continue(state: GraphState):
    if len(state["messages"]) > 6:
        return END
    return REFLECT 

builder.add_conditional_edges(GENERATE, should_continue, {END:END, REFLECT:REFLECT})
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()



if __name__ == '__main__':
    print("Hello langgraph")
    inputs = {"messages": [HumanMessage(content="Write a tweet about the weather in the next 200 characters")]}
    outputs = graph.invoke(inputs)
    print("--------------------------------")
    print(outputs)