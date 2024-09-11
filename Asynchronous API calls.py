import asyncio
import aiohttp
from aiolimiter import AsyncLimiter

limiter = AsyncLimiter(5, 60)


async def fetch_data(session, url):
    async with limiter:
        try:
         async with session.get(url) as response:
            print(f"Fetching {url} Status Code: {response.status}")
            if response.status != 200:
                response.raise_for_status()
            return await response.json()

        except aiohttp.ClientError as e:
            print(f"Client error occured for {url}:{e}")
        except Exception as e:
            print(f"An error occured for {url}:{e}")
        return None


async def fetch_all_data(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_data(session, url))
        return await asyncio.gather(*tasks)


urls = [
    "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=5",
    "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=6",
    "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=7",
    "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=8",
    "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=8",
]


async def main():
    results = await fetch_all_data(urls)
    for i, response in enumerate(results, 1):
        print(f"Response {i}: {response}")


asyncio.run(main())
