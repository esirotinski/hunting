import argparse

from utils.playwright_http_screenshot import save_screenshot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Saves screenshots of a domain.')
    parser.add_argument('domain', type=str, help='domain name.')
    args = parser.parse_args()

    if args.domain:
        save_screenshot(args.domain)
