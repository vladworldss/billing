from hashlib import sha256
from datetime import datetime


def create_handshake_id(user_id: int):
    now = datetime.now()
    msg = '{}:{}'.format(user_id, now.isoformat())
    res = sha256(msg.encode('utf-8')).hexdigest()

    return res
