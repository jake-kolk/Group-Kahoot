# Events
I haven't checked to make sure these signatures match with the server yet!
The types might be called something different!

## Client sends
- player_join: joins with a name and code
    - `{type: player_join, name: (string), room: (string)}`
- player_leave: Leaves using their id now.
    - `{type: player_leave, id: (int)}`
- answer_question
    - `{type: answer_question, id: (int), answer: (int)}`
- create_game `LATER`
- start_game: starts the game
    - `{type: start_game, name: (string), room: (string)}`
## Server sends
- start_game
- start_question: sends question to players with a timer to answer
    - `{type: start_question, question: (string), timer: (int)}`
- end_question
- player_joined: sends a message to other clients in the game about who joined
    - `{type: player_joined, name: (string)}`
- player_left: sends a message about who left
- game_end
