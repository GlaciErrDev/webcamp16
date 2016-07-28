import aiohttp
import asyncio


async def fetch(url, loop=None):
    with aiohttp.ClientSession(loop=loop) as client:
        async with client.get(url) as resp:
            assert resp.status == 200
            print('Requesting url', url)
            return await resp.text()


async def fetch_bad(url, loop=None):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            return response.read()


async def bound_fetch(semaphore, url, loop=None):
    async with semaphore:
        await fetch(url, loop)


async def fetch_everyting(loop=None):
    tasks = []
    sem = asyncio.Semaphore(100)
    for i in range(10000):
        tasks.append(bound_fetch(sem, 'http://127.0.0.1:8080/', loop))
    return await asyncio.gather(*tasks)


def main():
    loop = asyncio.get_event_loop()
    html = loop.run_until_complete(fetch_everyting(loop))


if __name__ == '__main__':
    main()
