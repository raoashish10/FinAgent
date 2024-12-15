from fastapi import FastAPI
from agent import graph
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

@app.get("/")
def query_llm(query: str) -> str:
    final_state = graph.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"configurable": {"thread_id": 42}}
    )
    last_message = final_state['messages'][-1].content
    return last_message