import os
import requests
import aiohttp
import asyncio
import argparse
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor


def extract_links_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

async def check_link(session: ClientSession, url: str):
    try:
        async with session.head(url, allow_redirects=True, timeout=10) as response:
            if response.status >= 400:
                return url, response.status
            return url, "OK"
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        return url, f"Error: {str(e)}"

async def check_links_concurrently(links):
    async with ClientSession() as session:
        tasks = [check_link(session, link) for link in links]
        return await asyncio.gather(*tasks)

# Function to scan a website or directory for broken links
def scan_website_or_directory(path_or_url):
    if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
        print(f"Scanning website: {path_or_url}")
        response = requests.get(path_or_url)
        if response.status_code != 200:
            print(f"Error: Unable to access {path_or_url} (Status code: {response.status_code})")
            return

        links = extract_links_from_html(response.content)
        absolute_links = [link if link.startswith('http') else path_or_url + link for link in links]

        asyncio.run(check_links_concurrently(absolute_links))

    else:
        print(f"Scanning local directory: {path_or_url}")
        html_files = []
        for root, dirs, files in os.walk(path_or_url):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        all_links = []
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as file:
                content = file.read()
                links = extract_links_from_html(content)
                all_links.extend(links)
        asyncio.run(check_links_concurrently(all_links))

def main():
    parser = argparse.ArgumentParser(description='Broken Link Checker')
    parser.add_argument('path_or_url', type=str, help='URL of the website or local directory path to scan for broken links.')
    args = parser.parse_args()

    scan_website_or_directory(args.path_or_url)

if __name__ == '__main__':
    main()
