"""
All imei_check enpoint dataclasses.
"""

from pydantic import BaseModel


class IMEIInfo(BaseModel):
    """{sku : article, storage : cost price}"""

    imei: str
    data: float


class IMEIInfoData(BaseModel):
    """
    Responce object containing marketplace cost price data.
    [{sku : article, storage : cost price},]
    """

    data: list[IMEIInfo]
