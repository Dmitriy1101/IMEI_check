"""
All imei_sandbox_check enpoint dataclasses.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class IMEIProperty(BaseModel):
    """properti data inside imei response"""

    deviceName: str
    image: str
    imei: int
    meid: int
    imei2: int
    serial: str
    estPurchaseDate: int
    repairCoverage: Optional[bool] = None
    replacement: Optional[bool] = None
    demoUnit: Optional[bool] = None
    apple_region: Optional[str] = Field(validation_alias="apple/region", default=None)
    apple_modelName: Optional[str] = Field(
        validation_alias="apple/modelName", default=None
    )
    loaner: Optional[bool] = None
    usaBlockStatus: Optional[str] = None
    network: Optional[str] = None


class IMEIService(BaseModel):
    """service data inside imei responce"""

    id: int
    title: str


class IMEISandboxInfo(BaseModel):
    """imei responce data"""

    id: str
    type: str
    status: str
    orderId: Optional[str] = None
    service: IMEIService
    amount: str
    deviceId: int
    processedAt: int
    properties: list[Optional[IMEIProperty]]

    @field_validator("properties", mode="before")
    @classmethod
    def normalize_properties(cls, value):
        """
        Преобразует properties в список, если это единственный объект IMEIPropertys.
        Если properties является None, возвращает пустой список.
        """
        if value is None:
            return []
        if isinstance(value, dict):
            return [IMEIProperty.model_validate(value)]
        if isinstance(value, list):
            return value
        raise ValueError("Invalid type. Expected list or dict.")


class IMEISandboxInfoData(BaseModel):
    """
    Responce object containing all imei responce data
    """

    data: list[IMEISandboxInfo]
