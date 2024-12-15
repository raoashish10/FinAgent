from langchain_core.tools import tool
import requests
import os
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


def get_retriever_tool():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings.client.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    db = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 1})
    retriever_tool = create_retriever_tool(
        retriever,
        "explain_financial_terms",
        "Explain financial terms in the query",)
    return retriever_tool


def news_helper(symbol: str, start_date: str, last_date: str):
    #   "c3smgt2ad3ide69e4jtg"
    FINNHUB_API_KEY = os.env["FINNHUB_API_KEY"]
    API_ENDPOINT = "https://finnhub.io/api/v1/company-news"
    queryString = f"{API_ENDPOINT}?symbol={symbol}&from={start_date}&to={last_date}&token={FINNHUB_API_KEY}"

    # Send the search query to the Search API
    response = requests.get(queryString)
    # Read the response
    articles = response.json()[-5:]
    summaries = [article["summary"] for article in articles]
    return ",".join(summaries)


@tool
def search_news_for_symbol(symbol: str, start_date: str, last_date: str) -> str:
    """Search for news articles in a time period for a given ticker symbol. eg: NVDA, MSFT, TSLA etc.

     Args:
          symbol: The symbol to search for.
          start_date: The start date of the search.
          last_date: The last date of the search.
    Returns:
          A string containing the news articles.
    """

    company_news = news_helper(
        symbol=symbol, start_date=start_date, last_date=last_date)
    return company_news


def get_tools():
    return [get_retriever_tool(), search_news_for_symbol]
