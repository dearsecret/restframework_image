import hashlib
import hmac
import base64
from config import settings
from urllib.parse import urlparse
from django.utils import timezone


def sms(to, content):
    url = f"https://sens.apigw.ntruss.com/sms/v2/services/{settings.SMS_SERVICE_ID}/messages"
    access_key = settings.SMS_ACCESS_KEY
    timestamp = f"{int(timezone.localtime(timezone.now()).timestamp()*1000)}"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": access_key,
        "x-ncp-apigw-signature-v2": make_signature(
            urlparse(url).path, access_key, timestamp
        ),
    }

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": f"{settings.SMS_NUMBER}",
        "content": content,
        "messages": [{"to": to}],
    }
    return {"url": url, "headers": headers, "json": body}


def make_signature(urn, access_key, timestamp):
    method = "POST"
    message = method + " " + urn + "\n" + timestamp + "\n" + access_key
    message = bytes(message, "UTF-8")
    signingKey = base64.b64encode(
        hmac.new(
            bytes(settings.SMS_SECRET_KEY, "UTF-8"), message, digestmod=hashlib.sha256
        ).digest()
    )
    return signingKey
