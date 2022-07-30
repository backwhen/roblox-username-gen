import asyncio
import random

import httpx
from rich import print

character_limit = int(input('Maximum number of characters in name: '))

limits = httpx.Limits(max_connections=5)
client = httpx.AsyncClient(
    limits=limits,
    timeout=None
)


def save(content: str) -> None:
    with open('output.txt', mode='a', encoding='utf-8') as f:
        f.write(f'{content}\n')


async def check(user: str) -> None:
    req = await client.get(f'https://auth.roblox.com/v2/usernames/validate?request.username={user}&request.birthday=01-01-2000&request.context=Signup')
    res = req.json()

    if 'message' in res and 'is valid' in res['message']:
        print(f'The username {user} is [bold green]available')
        save(user)
        return

    print(f'The username {user} is [bold red]already taken')


async def combine(word_list: list[str]) -> None:
    coros = []

    random.shuffle(word_list)
    for word in word_list:
        for word2 in reversed(word_list):
            user = f'{word}{word2}'
            if len(user) > character_limit:
                continue

            coros.append(check(user))

            if len(coros) == 10:
                await asyncio.gather(*coros)
                coros.clear()


async def main() -> None:
    req = await client.get('https://gist.githubusercontent.com/deekayen/4148741/raw')
    words = req.text.splitlines()
    await combine(words)

asyncio.run(main())
