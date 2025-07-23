import sys
import subprocess
from globals import current_user

#all strikes
STRIKES = ["jab", "cross", "lelbow", "relbow", "lkick", "rkick", "lknee", "rknee"]

def save_user_combo(combo_list):
    if not combo_list:
        return False
    combo_str = ",".join(combo_list)
    current_user["current_combo"] = combo_str
    return True