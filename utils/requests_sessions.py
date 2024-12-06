import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_h1_requests_session() -> requests.Session:
    token: str = os.getenv("H1_API_TOKEN")
    session = requests.Session()
    session.auth = ('sumbru', token)
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/122.0.6261.95 Safari/537.36',
        'X-Emergency': 'In case of emergency contact h@cker.md',
    })
    return session


def get_requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        # 'Content-Type': 'application/json',
        # 'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/122.0.6261.95 Safari/537.36',
        'X-Emergency': 'In case of emergency contact h@cker.md',
        'X-Bug-Bounty-Hunter': 'sumbru'
    })
    return session



if __name__ == '__main__':
    s = get_requests_session()
    response = s.get('https://httpbin.io/headers')
    print(response.text)