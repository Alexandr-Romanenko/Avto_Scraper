import asyncio

import aiohttp
from app.config.settings import settings


HEADERS = {"User-Agent": settings.app.user_agent}

# import asyncio
# import random
#
# async def retry(
#     coro,
#     retries: int = 3,
#     base_delay: float = 1.0,
#     factor: float = 2.0,
# ):
#     delay = base_delay
#
#     for attempt in range(retries):
#         try:
#             return await coro()
#         except asyncio.TimeoutError:
#             if attempt == retries - 1:
#                 raise
#         except Exception:
#             if attempt == retries - 1:
#                 raise
#
#         await asyncio.sleep(delay + random.uniform(0, 0.3))
#         delay *= factor
#
#
#
#
#
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


# async def fetch(http: aiohttp.ClientSession, url: str) -> str | None:
#     async with http.get(url, headers=HEADERS, timeout=30) as resp:
#             if resp.status != 200:
#                 return None
#             try:
#                 return await resp.text()
#             except Exception:
#                 print(f"Fetch failed: {url}")
#                 return None


async def fetch_list_page(http: aiohttp.ClientSession, url: str) -> str | None:
    return await fetch(http, url)
