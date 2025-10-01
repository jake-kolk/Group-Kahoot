# Events

## Client sends
- player_join: joins with a name and code
    - {type: player_join, name: (NAME), room: (ROOM)}
- player_leave
- answer_question
- create_game `LATER`

## Server sends
- start_game
- start_question: sends question to players with a timer to answer
- end_question
- player_joined: sends a message to other clients in the game about who joined
- player_left: sends a message about who left
- game_end