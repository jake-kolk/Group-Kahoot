# FLOW

### JOIN GAME
- client: `{type: join, room: (string), name: (string)}`
- server: `{type: joined, id: (int), room: (string)}`
- server: `{type: player_joined, id: (int), name: (string)}` for each player in lobby

### LEAVE GAME
- client: `{type: player_leave, room: (string)}`
- server: `{type: player_left, id: (int)}`

# Events
I haven't checked to make sure these signatures match with the server yet!
The types might be called something different!

## Client sends
- player_join: joins with a name and code  
    - `{type: player_join, room: (string), name: (string)}`
- player_leave: Leaves using their id now.  
    - `{type: player_leave, id: (int)}`
- answer_question  
    - `{type: answer_question, id: (int), answer: (int)}`
- create_game `LATER`
- start_game: starts the game  
    - `{type: start_game, room: (string), name: (string)}`
## Server sends
- start_game  
    - `{"type":"game_started"}`
- start_question: sends question to players with a timer to answer  
    - `{type: start_question, question: (string), timer: (int)}`
- end_question  
  - `{"type":"question_ended","player_answer_counts":answer_choice_counts}`
  - `{"type":"leaderboard","top":[]}`  
- player_joined: sends a message to other clients in the game about who joined
  - `{type: player_joined, name: (string)}`
- player_left:  
  - `{"type":"player_left","id":player_id}`
- game_end:  
  - `{"type":"game_end"}`
