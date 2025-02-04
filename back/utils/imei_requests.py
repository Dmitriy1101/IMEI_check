"""IMEI check api class"""

from fastapi import HTTPException
from requests import Response, get

from back.config import settings


class IMEICheck:
    """IMEI check api class"""

    def __init__(self, sandbox: bool = False) -> None:
        """Chose sandbox/live mode."""

        self.sandbox: bool = sandbox

    @property
    def token(self) -> str:
        """Choise token by mode."""

        if self.sandbox:
            return settings.TOKEN_SANDBOX
        else:
            return settings.TOKEN_LIVE

    @property
    def imei_check_url(self) -> str:
        """The amount of check will be charged from your account balance."""

        return "https://api.imeicheck.net/v1/checks"

    @property
    def imei_services_url(self) -> str:
        """Returns a list of Service objects."""

        return "https://api.imeicheck.net/v1/services"

    def headers(self) -> dict[str, str]:
        """:retutn: imei headers dict with auth token"""

        return {"Authorization": f"Bearer {self.token}", "Accept-Language": "en"}

    def params(self, imei: int | str) -> dict[str, str]:
        """:return: dict imei check request params"""

        return {"deviceId": str(imei), "serviceId": 15 if self.sandbox else 22}

    def check_imei(self, imei: int | str) -> list[dict]:
        """
        check imei using request to imei check api
        :return: list[dict] check imei data
        """

        resp: Response = get(
            url=self.imei_check_url,
            headers=self.headers(),
            params=self.params(imei=imei),
            timeout=10,
        )
        self.check_status(resp=resp)
        if self.sandbox:
            return [(i.pop("!!! WARNING !!!", "1") and i) for i in resp.json()]
        return resp.json()

    def service_list(self) -> list[dict]:
        """:return: list[dict] list of imei check servises."""

        resp = get(
            url=self.imei_services_url,
            headers=self.headers(),
            timeout=10,
        )
        self.check_status(resp=resp)
        return resp.json()

    def check_status(self, resp: Response) -> None:
        """Raise FastAPI exception by IMEI status code."""

        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Somefing wrong...")
