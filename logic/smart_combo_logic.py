#smart_combo_logic.py
import random
import sqlite3
from globals import current_user

#STRIKES list
STRIKES = ["jab", "cross", "lelbow", "relbow", "lkick", "rkick", "lknee", "rknee"]

#transition matrix
TRANSITIONS = {
    "Start": {"jab": 0.50, "cross": 0.20, "lelbow": 0.05, "relbow": 0.05, "lkick": 0.10, "rkick": 0.10, "lknee": 0.05, "rknee": 0.05},
    "jab": {"jab": 0.10, "cross": 0.48, "lelbow": 0.02, "relbow": 0.03, "lkick": 0.02, "rkick": 0.10, "lknee": 0.02, "rknee": 0.03},
    "cross": {"jab": 0.05, "cross": 0.11, "lelbow": 0.03, "relbow": 0.04, "lkick": 0.25, "rkick": 0.07, "lknee": 0.08, "rknee": 0.07},
    "lelbow": {"jab": 0.08, "cross": 0.08, "lelbow": 0.10, "relbow": 0.10, "lkick": 0.05, "rkick": 0.05, "lknee": 0.22, "rknee": 0.22},
    "relbow": {"jab": 0.08, "cross": 0.08, "lelbow": 0.10, "relbow": 0.10, "lkick": 0.05, "rkick": 0.05, "lknee": 0.22, "rknee": 0.22},
    "lkick": {"jab": 0.13, "cross": 0.20, "lelbow": 0.03, "relbow": 0.03, "lkick": 0.15, "rkick": 0.05, "lknee": 0.08, "rknee": 0.08},
    "rkick": {"jab": 0.13, "cross": 0.17, "lelbow": 0.03, "relbow": 0.03, "lkick": 0.05, "rkick": 0.15, "lknee": 0.08, "rknee": 0.08},
    "lknee": {"jab": 0.12, "cross": 0.14, "lelbow": 0.15, "relbow": 0.15, "lkick": 0.08, "rkick": 0.08, "lknee": 0.05, "rknee": 0.10},
    "rknee": {"jab": 0.12, "cross": 0.14, "lelbow": 0.15, "relbow": 0.15, "lkick": 0.08, "rkick": 0.08, "lknee": 0.10, "rknee": 0.05},
}

def weighted_choice(choices):
    items, weights = zip(*choices.items())
    return random.choices(items, weights=weights)[0]

def generate_smart_combo():
    length = random.choice([3, 4, 5])
    first = weighted_choice(TRANSITIONS["Start"])
    combo = [first]

    for _ in range(length - 1):
        last_strike = combo[-1]
        next_strike = weighted_choice(TRANSITIONS[last_strike])
        combo.append(next_strike)
    return combo
