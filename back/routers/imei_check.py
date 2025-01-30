"""
Endpoint '/api/cost_of_storage/{marketplace}' router
cost_of_storage endpoints.
"""

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from back.dataclass import IMEIInfo

# from src_public_api.db import get_cost_of_storage
# from src_public_api.db.bynary.requests import has_permission
# from src_public_api.schemas import CostOfStorageMarketplace, TablePermission
from back.utils import header_key

imei_check_router = APIRouter(prefix="/check-imei", tags=["check_imei"])


@imei_check_router.post(
    "/",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def imei_check(imei: int, authorization: str = Depends(header_key)) -> IMEIInfo:
    """Return marketplace cost of storage."""

    # await has_permission(
    #     token=authorization,
    #     table_name=TablePermission.COST_OF_STORAGE,
    #     code=marketplace.value,
    # )
    return IMEIInfo(imei="657657", data=0.01)
