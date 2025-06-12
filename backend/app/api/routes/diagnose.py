from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/diagnose", tags=["diagnose"])

# 模拟用户认证（暂不强制）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


class DiagnoseRequest(BaseModel):
    input_text: str  # 输入症状文本
    image_type: Optional[str] = None  # 图像类型（模拟用）


class DiagnoseResponse(BaseModel):
    agent_selected: str
    result: str
    needs_human_validation: bool


@router.post("/diagnose", response_model=DiagnoseResponse)
async def diagnose(
    request: DiagnoseRequest,
    token: str = Depends(oauth2_scheme)
):
    # 模拟 GPT 推理过程
    if "头痛" in request.input_text:
        agent = "脑部图像智能体"
        result = "疑似偏头痛，请进一步检查 MRI"
        needs_validation = True
    elif "咳嗽" in request.input_text:
        agent = "胸部 X 光智能体"
        result = "初步判断为轻微感染"
        needs_validation = False
    else:
        agent = "通用对话 Agent"
        result = "建议补充更多信息以继续诊断"
        needs_validation = False

    return DiagnoseResponse(
        agent_selected=agent,
        result=result,
        needs_human_validation=needs_validation
    )
