import requests
from .signature import sms


def send_sms(to: str, content: str):
    # SMS bytes 크기 90으로 제한된다.
    if len(content.encode()) < 90:
        try:
            res = requests.post(**sms(to, content))
            res.raise_for_status()
        except Exception as e:
            print(e)
