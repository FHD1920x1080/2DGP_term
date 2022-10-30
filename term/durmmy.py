table = {
    "SLEEP": {"HIT": "WAKE", "MOVE": "WAKE"},
    "WAKE": {"TIMER10": "SLEEP", "MOVE": "WAKE"}
}

cur_state = "SLEEP"

next_state = table[cur_state]["MOVE"] #"WAKE"
