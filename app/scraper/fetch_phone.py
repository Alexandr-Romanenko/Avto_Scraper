import asyncio

from aiohttp import ClientResponse, ClientSession, ClientTimeout, ClientResponseError, ClientError
from app.config.settings import settings


class PhoneClient:
    _lock = asyncio.Lock()

    def __init__(self, cookies: dict[str, str]):
        self.base_cookies = cookies
        self.session: ClientSession | None = None
        self.headers = {
            "user-agent": settings.app.user_agent,
            "content-type": "application/json",
            "x-ria-source": "vue3-1.39.2",
            "origin": "https://auto.ria.com",
            "referer": "https://auto.ria.com/",
        }

    async def __aenter__(self):
        self.session = ClientSession(
            headers=self.headers,
            cookies=self.base_cookies,
            timeout=ClientTimeout(total=10),
        )
        await self._refresh_phpsessid()
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def _get_fresh_phpsessid(self) -> str | None:
        async with ClientSession(headers={"User-Agent": settings.app.user_agent}) as s:
            async with s.get(settings.app.start_url) as r:
                cookie = r.cookies.get("PHPSESSID")
                return cookie.value if cookie else None

    async def _refresh_phpsessid(self) -> bool:
        async with self._lock:
            phpsessid = await self._get_fresh_phpsessid()
            if not phpsessid:
                return False

            assert self.session
            self.session.cookie_jar.update_cookies({"PHPSESSID": phpsessid})
            return True

    async def get_phone(
        self,
        auto_id: int,
        user_id: str,
        phone_id: str,
        retries: int = 2,
    ) -> str | None:

        payload = {
            "blockId": "autoPhone",
            "popUpId": "autoPhone",
            "autoId": auto_id,
            "data": [
                ["userId", user_id],
                ["phoneId", phone_id],
            ],
            "langId": 4,
            "device": "desktop-web",
        }

        for _ in range(retries):
            try:
                assert self.session
                resp: "ClientResponse"
                async with self.session.post(
                    "https://auto.ria.com/bff/final-page/public/auto/popUp/",
                    json=payload,
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("additionalParams", {}).get("phoneStr")

                    if resp.status in (401, 403):
                        await self._refresh_phpsessid()
                        continue

                    return None

            except ClientResponseError:
                await self._refresh_phpsessid()
            except asyncio.TimeoutError:
                print("phone timeout, retry")
            except ClientError:
                print("phone http error")


        return None
