import asyncio

import aiohttp
from app.config.settings import settings


HEADERS = {"User-Agent": settings.app.user_agent}

async def fetch(http: aiohttp.ClientSession, url: str) -> str | None:
    try:
        async with http.get(
            url,
            headers=HEADERS,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:

            if resp.status != 200:
                return None

            return await resp.text()

    except asyncio.TimeoutError:
        print(f"Timeout: {url}")
        return None

    except aiohttp.ClientError as e:
        print(f"HTTP error {url}: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error {url}: {e}")
        return None


async def fetch_list_page(http: aiohttp.ClientSession, url: str) -> str | None:
    return await fetch(http, url)
