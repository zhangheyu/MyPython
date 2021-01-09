import aiohttp
import asyncio
import time

async def fetch(client):
    async with client.get('https://python.org') as resp:
        assert resp.status == 200
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client)
        print(html)


if __name__ == '__main__':
    print(f"started at {time.strftime('%X')}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
