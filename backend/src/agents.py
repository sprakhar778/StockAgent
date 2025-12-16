import os
from dotenv import load_dotenv

from tools import get_stock_price,get_historical_stock_price,get_balance_sheet,get_stock_news


from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


model= ChatOpenAI(
    model="c1/openai/gpt-5/v-20251130",
    base_url="https://api.thesys.dev/v1/embed"
)

checkpointer=InMemorySaver()




agent=create_agent(
    model=model,
    checkpointer=checkpointer,
    tools=[get_stock_price,get_historical_stock_price,get_balance_sheet,get_stock_news]
)

