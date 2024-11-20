import concurrent.futures
import random
import dns.resolver
import argparse

from pathlib import Path
from multiprocessing import Pool
from utils.ChromeBrowser import ChromeBrowser
from utils.nameservers import nameservers
from utils.logger import logger


def resolve_dns(hostname, rtype):
    provider, servers = random.choice(list(nameservers.items()))
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = servers

    try:
        answers = resolver.resolve(hostname, rtype)
        for rdata in answers:
            logger.info(f'SUCCESS: {hostname} {answers.rdtype} {rdata}')
        with ChromeBrowser().browser as browser:
            try:
                browser.get('https://' + hostname)
                browser.save_screenshot(f'./screenshots/{hostname}.png')
            except Exception as e:
                logger.error(f'Failed to take screenshot for {hostname}', e)
    except dns.resolver.NoAnswer:
        logger.info(f'No answer for {hostname}')
    except dns.resolver.NXDOMAIN:
        logger.info(f'NXDOMAIN: {hostname}')
    except Exception as e:
        logger.error(f'ERROR resolving {hostname}: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script that resolves addresses.')
    parser.add_argument('domain', help='Domain starting with dot.')
    parser.add_argument('rtype', type=str, help='DNS resolution type. It could be A, CNAME, MX, etc.')
    parser.add_argument('processes', type=int, help='Number or parallel processes.')
    parser.add_argument('wordlist', help='Path to the wordlist file.')
    args = parser.parse_args()

    with open(Path(args.wordlist), encoding='utf-8') as file:
        subdomains = file.read().splitlines()
    fqdns = [str(subdomain) + args.domain for subdomain in set(subdomains)]

    # with Pool(processes=args.processes) as pool:
    #     pool.map(resolve_dns, fqdns)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.processes) as executor:
        executor.map(resolve_dns, *(fqdns, [args.rtype for _ in range(len(fqdns))]))
