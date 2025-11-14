import state

def generate_room_id():
    if not state.room_ids:
        raise ValueError("No more IDs available.")
    return state.room_ids.pop()

