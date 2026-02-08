from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from src.database import init_db, get_session
from src.services.auth import get_current_user_id

app = FastAPI(title="Todo AI Chatbot API")

@app.on_event("startup")
def on_startup():
    init_db()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID

from src.models.entities import Conversation, Message, MessageRole
from src.agents.todo_agent import execute_agent
from sqlmodel import select, Session
import json

@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    authenticated_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # 1. Get or create conversation
    if request.conversation_id:
        statement = select(Conversation).where(Conversation.id == request.conversation_id, Conversation.user_id == user_id)
        conversation = session.exec(statement).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
    
    # 2. Persist user message
    user_msg = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.message,
        user_id=user_id
    )
    session.add(user_msg)
    session.commit()
    
    # 3. Load history
    from src.services.history import get_conversation_history
    history = get_conversation_history(session, conversation.id)
    
    # 4. Execute agent
    # We pass history excluding the current message as it's already in 'message' arg
    # or pass full history if agent expects it.
    response_text, tool_calls = await execute_agent(request.message, history[:-1], user_id)
    
    # 5. Persist assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=response_text,
        user_id=user_id,
        tool_calls=json.dumps([t.dict() for t in tool_calls]) if tool_calls else None
    )
    session.add(assistant_msg)
    session.commit()
    
    return ChatResponse(
        response=response_text,
        conversation_id=conversation.id
    )

@app.get("/")
async def root():
    return {"message": "Phase III Todo AI Chatbot API"}