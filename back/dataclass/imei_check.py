"""
All imei_check enpoint dataclasses.
"""

from typing import Optional

from pydantic import BaseModel


class IMEIProperty(BaseModel):
    """properti data inside imei response"""

    deviceName: Optional[str] = None
    imei: Optional[str] = None
    modelName: Optional[str] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None


class IMEIService(BaseModel):
    """service data inside imei responce"""

    id: int
    title: str


class IMEIInfo(BaseModel):
    """imei responce data"""

    id: str
    type: str
    status: str
    orderId: Optional[str] = None
    service: IMEIService
    amount: str
    deviceId: int
    processedAt: int
    properties: Optional[IMEIProperty] = None


class IMEIInfoData(BaseModel):
    """
    Responce object containing all imei responce data
    """

    data: list[IMEIInfo]
