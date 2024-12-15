from utils.nodes import agent, tool_node, should_continue
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(MessagesState)
workflow.add_node("agent", agent)  # agent
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", 'agent')

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)