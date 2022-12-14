import asyncio

import httpx
from rich import print

word_list = input('Raw list of words to use (URL): ')
character_limit = int(input('Maximum number of characters in name: '))

client = httpx.AsyncClient(timeout=None)


def save(content: str) -> None:
    with open('output.txt', mode='a', encoding='utf-8') as f:
        f.write(f'{content}\n')


async def check(user: str) -> None:
    req = await client.get(f'https://auth.roblox.com/v2/usernames/validate?request.username={user}&request.birthday=01-01-2000&request.context=Signup')
    res = req.json()

    if 'message' in res and 'is valid' in res['message']:
        print(f'The username {user} is [bold green]available')
        return save(user)

    print(f'The username {user} is [bold red]already taken')


async def combine(word_list: list[str]) -> None:
    coros = []

    new_word_list = (word + word2 for word in word_list for word2 in reversed(word_list))
    for word in new_word_list:
        if len(word) > character_limit:
            continue

        coros.append(check(word))

        if len(coros) == 10:
            await asyncio.gather(*coros)
            coros.clear()

    await asyncio.gather(*coros)


async def main() -> None:
    req = await client.get(word_list)
    words = req.text.splitlines()
    await combine(words)

asyncio.run(main())
