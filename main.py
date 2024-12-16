from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from agent import get_graph
from langchain_core.messages import HumanMessage
from psycopg_pool import ConnectionPool
import os
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import MemorySaver

app = FastAPI()

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

@app.get("/")
def query_llm(query: str) -> str:
    with ConnectionPool(
    # Example configuration
    conninfo=os.environ['DB_URI'],
    max_size=20,
    kwargs=connection_kwargs,
    ) as pool:
        checkpointer = PostgresSaver(pool)
        # checkpointer = MemorySaver()
        checkpointer.setup()
        graph = get_graph(checkpointer)
        final_state = graph.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": "1"}}
        )
        last_message = final_state['messages'][-1].content
        return last_message