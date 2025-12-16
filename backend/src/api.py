from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.messages import SystemMessage, HumanMessage
from agents import agent

# Create a router 
router = APIRouter()


# ------------------ Request Models ------------------

class PromptObject(BaseModel):
    content: str
    id: str
    role: str


class RequestObject(BaseModel):
    prompt: PromptObject
    threadId: str
    responseId: str


# ------------------ API Route ------------------

@router.post("/api/chat")
async def chat(request: RequestObject):
    """
    Streaming chat endpoint compatible with TheSys C1Chat.
    """

    config = {"configurable": {"thread_id": request.threadId}}

    def generate():
        for token, _ in agent.stream(
            {
                "messages": [
                    SystemMessage(
                        "You are a business and stock analysis assistant. Your goal is to provide concise, accurate, "
                        "and well-structured information about companies and their stocks. "
                        "You have the ability to retrieve and analyze real-time stock prices, historical stock data, "
                        "company news, and balance sheet information for a given ticker symbol. "
                        "When responding: "
                        "- Use tables to present structured data such as financial highlights, key executives, "
                        "balance sheet summaries, and key metrics. "
                        "- Use graphs to visualize quantitative information such as stock price trends, revenue growth, "
                        "or financial performance over time. "
                        "- Use carousels to display product offerings or major business segments when applicable. "
                        "Keep responses concise, factual, and business-focused."
                    )
                    ,
                    HumanMessage(request.prompt.content),
                ]
            },
            stream_mode="messages",
            config=config,
        ):
            yield token.content

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Connection": "keep-alive",
        },
    )
