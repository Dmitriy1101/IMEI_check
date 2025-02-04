from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class IMEIInput(BaseModel):
    """imei and serial number string validator."""

    imei: str

    @field_validator("imei")
    @classmethod
    def validate_imei(cls, value: str) -> str:
        """
        IMEI validation or serial number.
        """

        _: tuple = (
            "Длина строки должна быть от 8 до 15 символов для ввода IMEI или серийного номера.",
            "Строка IMEI длиной 15 символов должна содержать только чисела.",
            "Строка серийного номера длиной от 8 до 14 символов содержит только буквы и цифры.",
        )
        if not 8 <= len(value) <= 15:
            raise HTTPException(status_code=400, detail=" ".join(_))
        if len(value) == 15 and not value.isdigit():
            raise HTTPException(status_code=400, detail=_[1])
        if 8 <= len(value) <= 14 and not value.isalnum():
            raise HTTPException(status_code=400, detail=_[2])
        return value
