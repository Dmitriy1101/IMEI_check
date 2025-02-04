"""
Endpoint '/api/cost_of_storage/{marketplace}' router
cost_of_storage endpoints.
"""

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from back.dataclass import IMEISandboxInfoData
from back.db.bynary.request import has_permission
from back.schema import AccessType
from back.utils import IMEICheck, header_key

imei_check_sandbox_router = APIRouter(prefix="/check-imei-sandbox", tags=["check_imei"])


@imei_check_sandbox_router.post(
    "/",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def imei_check_sandbox(
    imei: int, authorization: str = Depends(header_key)
) -> IMEISandboxInfoData:
    """Return sandbox imei check result."""

    await has_permission(
        token=authorization,
        acsess_type=AccessType.IMEI_CHECK,
        code="ALL",
    )
    return IMEISandboxInfoData(data=IMEICheck(sandbox=True).check_imei(imei=imei))
