import requests
from .signature import sms


def send_sms(to: str, content: str):
    try:
        res = requests.post(**sms(to, content))
        res.raise_for_status()
    except Exception as e:
        print(e)
