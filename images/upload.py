from config import settings
import requests
import asyncio

# from time import time

url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1/direct_upload"


def get_link():
    res = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.CF_TOKEN}",
            "Content-Type": "application/json",
        },
        data={"requireSignedURLs": "true"},
    )
    print(res.text)
    if res.status_code == 200:
        link = res.json().get("result")
        return link.get("uploadURL")


async def get_urls(cnt):
    # s = time()
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, get_link) for _ in range(cnt)]
    result = await asyncio.gather(*tasks)
    # print(time() - s)
    return result


def get_links(cnt: int = 1):
    result = asyncio.run(get_urls(cnt))
    return result


def check_status(id):
    url = (
        f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1/{id}"
    )
    res = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.CF_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    return res
