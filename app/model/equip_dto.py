from pydantic import BaseModel, Field
from typing import List, Optional

class EquipRsvrRequest(BaseModel):
    # 필수 파라미터: 설비 시퀀스
    equip_sq: int = Field(..., description="설비 시퀀스 번호", example=101)

class EquipRsvrResponse(BaseModel):
    # 조회 결과 응답 모델 (예시)
    rsvr_id: str
    rsvr_name: str
    capacity: float
    status: Optional[str] = "NORMAL"

    class Config:
        from_attributes = True