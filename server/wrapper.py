import state as state
import jwt
from jose import jwt, JWTError
import secrets
import datetime
from models import GameRoom, Host
import ssl
from state import rooms
from models import Session
import random
from datetime import datetime, timezone, timedelta
import os

# Dynamically locate file given start dir and file name
# I made this because CWD can vary depending on where the server is launched from
def find_file(start_dir, target_filename): 

    for root, dirs, files in os.walk(start_dir):
        if target_filename in files:
            return os.path.join(root, target_filename)
    return None

def init_server():
    state.SECRET_KEY = secrets.token_urlsafe(32)

    CWD = os.getcwd()
    cert_path = find_file(CWD, "cert.pem")
    key_path = find_file(CWD, "key.pem")
    state.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    state.ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    state.room_ids = list(range(100001, 1000000)) # Generate set of room sids (7mb in memory)
    random.shuffle(state.room_ids)


def generate_game_token( user_id: int):
    payload = {
    "user_id": user_id,
    "iat": datetime.now(timezone.utc),  # issued at
    "exp": datetime.now(timezone.utc) + timedelta(60)  # expires in 60 min
    }

    token = jwt.encode(payload, state.SECRET_KEY, algorithm="HS256")
    state.hosts[user_id] = token
    return token


async def create_game(sessionOBJ: int, question_set: int, time_limit: int, question_count: int, auth: str):
    try:
        new_host = Host(sessionOBJ, auth)
        new_gameroom = GameRoom(question_set, time_limit, question_count, new_host)

        new_gameroom.host = new_host
        room_number = new_gameroom.room_number

        state.hosts[auth] = room_number
        print("auth registered as" + str(auth))
        state.rooms[room_number] = new_gameroom

        await sessionOBJ.send({"type": "game_created", "room_number": room_number, "success": True})
    except Exception as ex:
        print(str(ex))
        await sessionOBJ.send({"type": "game_created", "success": False})