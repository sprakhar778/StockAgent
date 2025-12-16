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
                        "You are a stock price analysis assistant. "
                        "You have ability to get real-time stock price, "
                        "historical stock-price, news and balance sheet "
                        "data on a given ticker symbol."
                    ),
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
