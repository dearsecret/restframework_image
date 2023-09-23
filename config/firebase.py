import os
from . import settings
import time
from datetime import timedelta
from uuid import uuid4

from firebase_admin import firestore, initialize_app, credentials

# __all__ = ["send_to_firebase", "update_firebase_snapshot"]
__all__ = ["send_to_firebase"]

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "firebase_config.json"))
initialize_app(cred)


def send_to_firebase(raw_notification):
    db = firestore.client()
    start = time.time()
    db.collection("chats").document(str(uuid4())).create(raw_notification)
    end = time.time()
    spend_time = timedelta(seconds=end - start)
    return spend_time


# def update_firebase_snapshot(snapshot_id):
#     start = time.time()
#     db = firestore.client()
#     db.collection("chats").document(snapshot_id).update({"is_read": True})
#     end = time.time()
#     spend_time = timedelta(seconds=end - start)
#     return spend_time
