from tools import get_tools
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState
from typing import Literal

tools = get_tools()
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)


def agent(state: MessagesState):
    messages = state['messages']
    response = llm.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END