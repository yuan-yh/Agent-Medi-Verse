import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.user import User  # 如果有循环引用可以延迟 import

class Diagnose(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    input_text: str
    agent_selected: str
    result: str
    needs_human_validation: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 关系字段（反向引用）
    owner: Optional["User"] = Relationship(back_populates="diagnoses")
    messages: List["ChatMessage"] = Relationship(back_populates="diagnose")
