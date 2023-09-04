import hmac
import hashlib
from urllib.parse import urlparse
from datetime import datetime
from config import settings


# from django.utils import timezone 아닌 cloudflare는
# UTC 기준 timestamp 입니다.
# expiry 는 Seconds 기준
# expiry = int(timezone.now().timestamp() + 60*60*24)
# browser TTL 은 미설정


def make_signautre(url: str, exp: int = 60):
    exp = int(datetime.now().timestamp() + exp)
    string_to_sign = urlparse(url).path + f"?exp={exp}"

    sig = hmac.new(
        bytes(settings.CF_KEY, "utf-8"),
        msg=bytes(string_to_sign, "utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    url = url + f"?exp={exp}&sig={sig}"
    print(url)
    return url
