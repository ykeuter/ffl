from ffl import models

STARTERS = {"QB": 1, "WR": 2, "RB": 2, "FLEX": 1, "TE": 1, "EDR": 1, "D": 1,
        "K": 1}

class state():
    def __init__(self, rosters, turns, freeagents):
        self.rosters = rosters
        self.turns = turns
        self.freeagents = freeagents


