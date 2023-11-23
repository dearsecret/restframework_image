import os
import io
from PIL import Image
import time
import requests
from uuid import uuid4
from datetime import timedelta
from . import settings
from django.utils.timezone import now

from firebase_admin import firestore, initialize_app, credentials, storage, auth, db

# __all__ = ["send_to_firebase", "update_firebase_snapshot"]
__all__ = ["send_to_firebase", "send_to_database"]
# db.reference("posts").set({"pk" : value})

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "firebase_config.json"))
initialize_app(
    cred,
    {
        "databaseURL": "https://dating-chats-dearsecret-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)


def send_to_database(ref: str, data: dict):
    # changeListenr 처리
    # TODO : TRY && EXCEPT 구문
    db.reference(ref).set(data)


def update_to_database(data: dict):
    db.reference("posts").child(data["pk"]).update({data["pk"]: data})


def send_to_firebase(data):
    fs = firestore.client()
    fs.collection("chats").document(str(uuid4())).create(data)
    print("sucees")


# def update_firebase_snapshot(snapshot_id):
#     start = time.time()
#     db = firestore.client()
#     db.collection("chats").document(snapshot_id).update({"is_read": True})
#     end = time.time()
#     spend_time = timedelta(seconds=end - start)
#     return spend_time


def send_to_comment(id, comment, user):
    db = firestore.client()
    start = time.time()
    db.collection("chats").document(id).collection("comment").document(
        str(uuid4())
    ).create(
        {
            "comment": comment,
            "user": f"{user}",
            "timestamp": now(),
        }
    )
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time


def send_to_storage(pk, url):
    client = storage.Client()
    bucket = client.get_bucket("bucket-id-here")
    blob = bucket.blob("remote/path/storage.txt")
    # make_signature
    res = requests.get(url)

    bs = io.BytesIO(res.content)
    im = Image.open(bs)
    im.save(bs, "png")

    blob.upload_from_filename(bs.getValue(), content_type="image/png")


def make_custom_token(uid):
    return auth.create_custom_token(uid)
