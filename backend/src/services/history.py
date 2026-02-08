from sqlmodel import Session, select
from src.models.entities import Message
from uuid import UUID

def get_conversation_history(session: Session, conversation_id: UUID, limit: int = 20):
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    history = session.exec(statement).all()
    # Reverse to get chronological order
    return history[::-1]
