import asyncio
from collections import deque
import json
import logging
from state import rooms
import random
#import requests

class Session:
    """
    One websocket connection. Holds player_id and name after joining.
    Each player has uniqe session, uses to keep connections open
    """
    def __init__(self, websocket):
        self.ws = websocket
        self.name = ""
        self.player_id = -1
        self._write_queue = deque()
        self._write_lock = asyncio.Lock()

    async def send(self, j):
        message = json.dumps(j)
        async with self._write_lock:
            await self.ws.send(message)

class Player:
    def __init__(self, session, name, player_id):
        self.sess = session
        self.name = name
        self.id = player_id
        self.points = 0

class GameRoom:

    def __init__(self, code):
        self.code = code
        self.players = dict()
        self.next_player_id = 1
        self.current_question_id = -1
        self.answers_received = {}
        self.timer_task = None
        self.gameStarted = False
        # self.questions = []
        self.question_answer_window_seconds = 10 # Kinda long if you think of something better please replace
        question = {"text": "What's 2+2?", "choices": ["1", "3", "4", "5"]}
        self.questions = [question.copy() for _ in range(10)]

        
    async def broadcast(self, j):
    # Use Session.send() so per-connection locking is preserved,
    # but run all sends concurrently so one slow client doesn't block others.
        await asyncio.gather(
        *(p.sess.send(j) for p in self.players.values()),
        return_exceptions=True
        )



    async def add_player(self, session, data):
        name = data.get("name","guest")
        room_code = data.get("room")
        player_id = self.next_player_id

        if str(room_code) not in rooms:
            logging.error("ERROR: handler: roomnum " + str(room_code) + "NOT FOUND")
            return
        
        roomObj = rooms[room_code]
        await session.send({"type":"joined","id":self.next_player_id,"room":room_code}) #tell client they  joined
    
        self.next_player_id += 1
        
        #init session & player objects
        self.players[player_id] = Player(session, name, player_id)

        session.player_id = player_id
        session.name = name

        await self.broadcast({"type":"player_joined","id":player_id,"name":name}) #tell all others in room player joined
        return

    async def remove_player(self, session: Session, data):
        room_code = data.get("room")
        player_id = session.player_id

        if str(room_code) not in rooms:
            logging.error("ERROR: handler: roomnum " + str(room_code) + "NOT FOUND")
            return
        
        roomObj = rooms[room_code]
    
        if player_id > 0 and player_id in self.players:
            del self.players[player_id]
            await self.broadcast({"type":"player_left","id":player_id})
            # If player leaving results in empty GameRoom, end game
            if len(self.players) == 0: 
                logging.info("Room num" + str(self.code)  + " ended due to 0 players")
                await self.end_game()

    def load_questions_from_db():
        try:
            # URL points to your database container
            response = requests.get("http://localhost:8000/questions")
            response.raise_for_status()
            questions = response.json()
            print(f"Loaded {len(questions)} questions from DB")
            return questions
        except Exception as e:
            print("Error fetching questions from DB:", e)
            return []

    async def end_game(self):
        self.gameStarted = False
        self.current_question_id = 0
        if str(self.code) != "100000":  # We dont want to delete default room
            rooms.pop(str(self.code), None) # Pops room from rooms, if room nonexistant does not raise error
        else:
            logging.info("end_game: default game end attempted!")
    
    async def start_game(self, session: Session, data):
        roomCode = data.get("room")

        if str(roomCode) not in rooms:
            logging.error("ERROR: handler: roomnum " + str(roomCode) + "NOT FOUND")
            return
        
        self.current_question_id = 0
        self.gameStarted = True

        # Start main game loop
        # await self.run_game()
            # Start main game loop in background so the websocket handler stays responsive
        if not hasattr(self, "game_task") or self.game_task.done():
            self.game_task = asyncio.create_task(self.run_game())
            

    async def start_question(self):
        question_id = self.current_question_id
        question = {"text":"What's 2+2?","choices":["1","3","4","5"]}
        roomCode = self.code

        if str(roomCode) not in rooms:
            logging.error("ERROR: handler: roomnum " + str(roomCode) + "NOT FOUND")
            return
        else:
            roomObj = rooms[roomCode]

        msg = dict(question)
        msg["type"] = "question"
        msg["question_id"] = question_id
        msg["duration_ms"] = self.question_answer_window_seconds * 1000
        self.current_question_id = question_id
        self.answers_received.clear()
        await self.broadcast(msg)

    async def _end_question_after(self, seconds):
        try:
            await asyncio.sleep(seconds)
            await self.end_question()
        except asyncio.CancelledError:
            pass


    async def handle_answer(self, session: Session, data):
        player_id = session.player_id
        question_id = data.get("question_id",-1)
        choice = data.get("choice",-1)
        time_left_ms = data.get("time_left_ms",0)
        roomCode = data.get("room")

        if str(roomCode) not in rooms: # Make sure room code is valid
            logging.error("ERROR: handle_answer: roomnum " + str(roomCode) + " not found!")
            return
        if question_id != self.current_question_id: # Make sure answer is to current question.
            logging.error("ERROR: handle_answer: questionID != current question id(answer for wrong question receved)")
            return
        if player_id in self.answers_received: # Make sure there is no double answer
            logging.error("ERROR: handle_answer: playerid in answeres receved (multiple answers sent)")
            return
        
        self.answers_received[player_id] = (choice, time_left_ms)
        await self.players[player_id].sess.send({"type":"answer_ack","ok":True})

        # Check if all players have answered, if so end question
        if len(self.answers_received) >= len(self.players):
            if self.timer_task:
                self.timer_task.cancel()

    async def end_question(self,):
        correct_choice = 3  # for demo
        answer_choice_counts = [0,0,0,0]

        # Tally up who picked what answer
        for choice, _ in self.answers_received.values(): 
            if 0 <= choice < len(answer_choice_counts):
                answer_choice_counts[choice] += 1

        # Evaluate if answer was correct and add points
        for player_id,(choice,time_left_ms) in self.answers_received.items():
            if choice == correct_choice:
                base = 1000
                bonus = max(0, time_left_ms*1000//100)
                self.players[player_id].points += base + bonus

        await self.broadcast({"type":"question_ended","player_answer_counts":answer_choice_counts})

        # Create and sort leaderboard
        leaderboard = {"type":"leaderboard","top":[]}
        leaderboard["top"] = sorted(
        [
            {"id": p.id, "name": p.name, "points": p.points}
            for p in self.players.values()
        ],
        key=lambda x: x["points"],
        reverse=True
        )
        for player in self.players.values:
            leaderboard["top"].append({"id":player.id,"name":player.name,"points":player.points})
        await self.broadcast(leaderboard)

        # Question ended and leaderboards sent
        self.current_question_id += 1
        
  
    async def _start_question_after(self, session, data, seconds):
        try:
            await asyncio.sleep(seconds)
            #Look in data base and get question 1, for now ill supply dummy question info
            q = {"text":"What's 2+2?","choices":["1","3","4","5"]}
            await self.start_question(session, data)
        except asyncio.CancelledError:
            pass

    async def create_room(self, session:Session, data):
        while roomNum in rooms:
            roomNum = random.randint(100000, 999999) #generate new room num if new room num is taken

    async def run_game(self):
        # Start question
        while self.current_question_id < len(self.questions):
            await self.start_question()

            
            # Clear old timer
            if self.timer_task and not self.timer_task.done():
                self.timer_task.cancel()

            # End question & send out leaderboard (included in end question)
            self.timer_task = asyncio.create_task(self._end_question_after(self.question_answer_window_seconds))
            # Code below pauses execution untill task is over or timer canceled and end_question is called elsewhere
            try:
                await self.timer_task 
            except asyncio.CancelledError:
                await self.end_question()

            # Wait 5s so players can see leaderboard and get ready for next question
            await asyncio.sleep(5)

            # Repeat if questions are remaining

        await self.end_game()