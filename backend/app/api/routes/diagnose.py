from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select, Session
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.api.deps import SessionDep, CurrentUser
from app.models import Diagnose, ChatMessage, User

router = APIRouter(prefix="/diagnose", tags=["diagnose"])

# 请求体结构
class DiagnoseRequest(BaseModel):
    input_text: str


# 返回结构
class DiagnosePublic(BaseModel):
    id: UUID
    agent_selected: str
    result: str
    needs_human_validation: bool
    created_at: datetime


@router.post("/", response_model=DiagnosePublic)
def create_diagnosis(
    session: SessionDep,
    current_user: CurrentUser,
    body: DiagnoseRequest
) -> Any:
    """
    创建一次诊断，并记录用户输入与 AI 回复
    """

    user_input = body.input_text

    # 模拟智能体选择逻辑（将来接入 LLM）
    if "咳嗽" in user_input:
        agent = "胸部图像 Agent"
        result = "建议拍摄胸部 X 光片，疑似轻微感染"
        needs_validation = True
    elif "头痛" in user_input:
        agent = "脑部图像 Agent"
        result = "建议 MRI 检查，排查偏头痛或颅压问题"
        needs_validation = True
    else:
        agent = "通用问答 Agent"
        result = "请补充更多症状信息以便进一步分析"
        needs_validation = False

    # 创建诊断记录
    diagnose = Diagnose(
        owner_id=current_user.id,
        input_text=user_input,
        agent_selected=agent,
        result=result,
        needs_human_validation=needs_validation,
    )
    session.add(diagnose)
    session.commit()
    session.refresh(diagnose)

    # 写入聊天记录（用户输入）
    user_msg = ChatMessage(
        diagnose_id=diagnose.id,
        sender="user",
        message=user_input
    )
    session.add(user_msg)

    # 写入聊天记录（AI 回复）
    ai_msg = ChatMessage(
        diagnose_id=diagnose.id,
        sender="assistant",
        message=result
    )
    session.add(ai_msg)

    session.commit()

    return DiagnosePublic(
        id=diagnose.id,
        agent_selected=agent,
        result=result,
        needs_human_validation=needs_validation,
        created_at=diagnose.created_at
    )
