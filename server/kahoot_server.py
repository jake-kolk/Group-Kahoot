# kahoot_server.py
# Run: python3 kahoot_server.py
# Requires: pip install websockets

import asyncio
import json
import traceback
from collections import deque

class Session:
    """
    One websocket connection. Holds player_id and name after joining.
    """
    def __init__(self, websocket):
        self.ws = websocket
        self.name = ""
        self.player_id = -1
        self._write_queue = deque()
        self._write_lock = asyncio.Lock()

    async def send(self, j):
        txt = json.dumps(j)
        async with self._write_lock:
            await self.ws.send(txt)

class Player:
    def __init__(self, sess, name, pid):
        self.sess = sess
        self.name = name
        self.id = pid
        self.points = 0

class GameRoom:
    def __init__(self, code):
        self.code = code
        self.players = {}
        self.next_player_id = 1
        self.current_question_id = -1
        self.answers_received = {}
        self.timer_task = None

    async def broadcast(self, j):
        for p in self.players.values():
            try:
                await p.sess.send(j)
            except:
                # ignore failed sends
                pass

    async def add_player(self, s: Session, name: str):
        pid = self.next_player_id
        self.next_player_id += 1
        self.players[pid] = Player(s, name, pid)
        s.player_id = pid
        s.name = name
        await self.broadcast({"type":"player_joined","id":pid,"name":name})
        return pid

    async def remove_player(self, s: Session):
        pid = s.player_id
        if pid > 0 and pid in self.players:
            del self.players[pid]
            await self.broadcast({"type":"player_left","id":pid})

    async def start_question(self, question_id, question_payload, duration_ms):
        msg = dict(question_payload)
        msg["type"] = "question"
        msg["question_id"] = question_id
        msg["duration_ms"] = duration_ms
        self.current_question_id = question_id
        self.answers_received.clear()
        await self.broadcast(msg)

        # cancel any existing timer
        if self.timer_task and not self.timer_task.done():
            self.timer_task.cancel()

        self.timer_task = asyncio.create_task(self._end_question_after(duration_ms/1000))

    async def _end_question_after(self, seconds):
        try:
            await asyncio.sleep(seconds)
            await self.end_question()
        except asyncio.CancelledError:
            pass

    async def handle_answer(self, player_id, question_id, choice, time_left_ms):
        if question_id != self.current_question_id:
            return
        if player_id in self.answers_received:
            return
        self.answers_received[player_id] = (choice, time_left_ms)
        await self.players[player_id].sess.send({"type":"answer_ack","ok":True})
        if len(self.answers_received) >= len(self.players):
            if self.timer_task:
                self.timer_task.cancel()
            await self.end_question()

    async def end_question(self):
        correct_choice = 1  # for demo
        counts = [0,0,0,0]
        for choice, _ in self.answers_received.values():
            if 0 <= choice < len(counts):
                counts[choice] += 1
        for pid,(choice,time_left_ms) in self.answers_received.items():
            if choice == correct_choice:
                base = 1000
                bonus = max(0, time_left_ms*1000//100)
                self.players[pid].points += base + bonus
        await self.broadcast({"type":"question_ended","counts":counts})
        lb = {"type":"leaderboard","top":[]}
        for pr in self.players.values():
            lb["top"].append({"id":pr.id,"name":pr.name,"points":pr.points})
        await self.broadcast(lb)

room = GameRoom("ROOM!")

async def handler(websocket):
    s = Session(websocket)
    try:
        async for raw in websocket:
            try:
                j = json.loads(raw)
            except:
                print("json parse error", raw)
                continue
            t = j.get("type","")
            if t == "join":
                name = j.get("name","guest")
                pid = await room.add_player(s, name)
                await s.send({"type":"joined","id":pid,"room":room.code})
            elif t == "answer":
                qid = j.get("question_id",-1)
                choice = j.get("choice",-1)
                time_left = j.get("time_left_ms",0)
                await room.handle_answer(s.player_id,qid,choice,time_left)
            elif t == "start_question":
                qid = j.get("question_id",1)
                q = {"text":"What's 2+2?","choices":["1","3","4","5"]}
                await room.start_question(qid,q,15000)
    except:
        traceback.print_exc()
    finally:
        await room.remove_player(s)

import websockets

async def main():
    print("Server running on :8080")
    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
