from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from uuid import UUID

from app.api.deps import SessionDep, CurrentUser
from app.models import Diagnose, DiagnoseCreate, DiagnosePublic

router = APIRouter(prefix="/diagnose", tags=["diagnose"])


@router.post("/", response_model=DiagnosePublic)
def diagnose(
    session: SessionDep,
    current_user: CurrentUser,
    body: DiagnoseCreate
) -> Any:
    # 模拟 Agent 判断
    if "头痛" in body.input_text:
        agent = "脑部图像智能体"
        result = "疑似偏头痛，请进一步检查 MRI"
        need_validation = True
    else:
        agent = "通用问答 Agent"
        result = "请补充更多信息以判断"
        need_validation = False

    record = Diagnose(
        owner_id=current_user.id,
        input_text=body.input_text,
        agent_selected=agent,
        result=result,
        needs_human_validation=need_validation,
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
