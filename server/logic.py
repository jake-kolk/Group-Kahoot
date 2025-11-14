# kahoot_server.py
# Run: python3 kahoot_server.py
# Requires: pip install websockets

import asyncio
import json
import traceback
from collections import deque
import logging
import config
from models import GameRoom
from models import Session
from state import rooms
import wrapper
from wrapper import create_game
import state
import os

player_requests = {
    # Player commands
    "join" : GameRoom.add_player,
    "player_leave": GameRoom.remove_player,
    "answer" : GameRoom.handle_answer,
    "start_questions" : GameRoom.start_question,
}

host_requests = {
    # Host commands
    "start_game" : GameRoom.start_game,
    "create_game" : create_game
}

db_server_requests = {
    "get_game_token" : wrapper.generate_game_token
}

wrapper.init_server()

async def handle_host(data: dict, sessionOBJ: Session, requestType: str):
    try:
        # Auth 
        auth = data.get("auth")
        if auth in state.hosts: #handler for everything else
            roomObj = state.rooms[state.hosts[auth]] #  This is weird, but it looks up room number with auth(token), then uses room_num to get roomOBJ
            await host_requests[requestType](roomObj, sessionOBJ, data)
        elif requestType == "create_game": # handler for create_game
                question_set = data.get("question_set")
                time_limit = data.get("time_limit")
                question_count = data.get("question_count")
                await host_requests[requestType](sessionOBJ, question_set, time_limit, question_count, auth)
        else:
            logging.error("logic.py: handle_host: cannot find auth " + str(data.get("auth"))) # Error handler
            await sessionOBJ.send({"error": "room_not_found"})
    except Exception as exc:
        print("[ERROR] handle_host: locic.py: " + str(exc))

async def handle_player(data: dict, sessionOBJ: Session, requestType: str):
    if data.get("room") in rooms:
        roomObj = rooms[data.get("room")]
        await player_requests[requestType](roomObj, sessionOBJ, data)
    else:
        logging.error("lgoic.py: handle_player: cannot find room " + str(data.get("room")))
        sessionOBJ.send({"error": "room_not_found"})

async def handle_auth(data: dict, sessionOBJ: Session, requestType: str): # This is only hit by db server
    user_id = data.get("user_id")
    token = wrapper.generate_game_token(int(user_id))
    await sessionOBJ.send({"auth_token": token})

async def handler(websocket):
    sessionOBJ = Session(websocket)
    try:
        async for raw in websocket:
            try:
                data = json.loads(raw)
            except:
                print("json parse error", raw)
                continue
            requestType = data.get("type","")
            if requestType in host_requests:
                await handle_host(data, sessionOBJ, requestType)
            elif requestType in player_requests:
                await handle_player(data, sessionOBJ, requestType)
            elif requestType in db_server_requests:
                await handle_auth(data, sessionOBJ, requestType)
            else:
                logging.error("HANDLER: cannot find request: " + str(requestType))
                sessionOBJ.send({"error": "invalid_request"})
                 
    except:
        traceback.print_exc()


import websockets

async def main():
    print("Server running on :8080")

    # Starts WSS (secure) with ssl
    async with websockets.serve(handler, "0.0.0.0", 8080, ssl=state.ssl_context):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
