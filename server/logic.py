# kahoot_server.py
# Run: python3 kahoot_server.py
# Requires: pip install websockets

import asyncio
import json
import traceback
from collections import deque
import logging
#import requests
import config
from models import GameRoom
from models import Session
from state import rooms
#####GLOBAL ROOM STORAGE (probably want to optimize later)
    #init  rooms


rooms["100000"] = GameRoom("100000") #this is default for testing

requests = {
    "join" : GameRoom.add_player,
    "player_leave": GameRoom.remove_player,
    "answer" : GameRoom.handle_answer,
    "start_questions" : GameRoom.start_question,
    "start_game" : GameRoom.start_game,
    "create_game" : GameRoom.create_room

}
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
            if requestType in requests:
                if data.get("room") in rooms:
                    roomObj = rooms[data.get("room")]
                    await requests[requestType](roomObj, sessionOBJ, data)
                else:
                    logging.error("HANDLER: cannot find room " + str(data.get("room")))
            else:
                logging.error("HANDLER: cannot find request: " + str(requestType))
                 
    except:
        traceback.print_exc()


import websockets

async def main():
    print("Server running on :8080")


    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
