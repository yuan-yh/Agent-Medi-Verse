import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.diagnose import Diagnose  # 避免 import 循环问题时可以延迟导入

class ChatMessage(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    diagnose_id: uuid.UUID = Field(foreign_key="diagnose.id", nullable=False)
    sender: str  # user / assistant
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    diagnose: Optional["Diagnose"] = Relationship(back_populates="messages")
