from fastapi import APIRouter
from app.core.gst import GSTService
from app.core.gst.schemas import GSTINValidationResult, GSTStateResponse
from app.core.gst.state_codes import GSTStateMaster
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/gst", tags=["GST"])

@router.get("/validate/{gstin}")
def validate_gstin(gstin: str) -> ApiResponse[GSTINValidationResult]:
    result = GSTService.validate(gstin)
    return ApiResponse(success=True, data=result)

@router.get("/states")
def list_states() -> ApiResponse[list[GSTStateResponse]]:
    states = GSTStateMaster.all_states()
    return ApiResponse(success=True, data=[GSTStateResponse(**s) for s in states])

@router.get("/states/{code}")
def get_state(code: str) -> ApiResponse[GSTStateResponse | None]:
    state = GSTStateMaster.get_state(code)
    if not state:
        return ApiResponse(success=False, data=None)
    return ApiResponse(success=True, data=GSTStateResponse(**state))
