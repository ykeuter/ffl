from ffl import models
import numpy as np

class FreeAgent:
    def __init__(self, id, name, team, positions, points):
        pos_map = [
                    ("DL", {"DE", "DT"}),
                    ("DB", {"S", "CB"}),
                    ("K", {"K"}),
                    ("D", {"D"}),
                    ("TE", {"TE"}),
                    ("WR", {"WR"}),
                    ("RB", {"RB"}),
                    ("QB", {"QB"}),
                  ]
        self.espn_id = id
        self.name = name
        self.team = team
        self.positions = positions
        self.position = next(p for p, ps in pos_map
            if set(positions).intersection(ps))
        self.points = points

def getFreeAgents():
    FA_STRING = "FA"
    DEF_STRING = "D"

    fa = [FreeAgent(p.espn_id, p.name,
        p.team.espn_code if p.team else FA_STRING,
        [pos.espn_code for pos in p.positions],
        p.projected_points) for p in models.NflPlayer.query.all() if
        p.projected_points is not None]
    fa += [FreeAgent(t.espn_id, t.name, t.espn_code, [DEF_STRING],
        t.projected_defense_points) for t in
        models.NflTeam.query.all()]
    return sorted(fa, key=lambda p: -p.points)

class GameState:
    def __init__(self, rosters, turns, freeagents, playerjm=None):
        self.rosters = rosters
        self.turns = turns
        self.freeagents = freeagents
        self.playerJustMoved = playerjm

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        rosters = [r[:] for r in self.rosters]
        st = GameState(rosters, self.turns[:], self.freeagents[:],
                self.playerJustMoved)
        return st

    def PickFreeAgent(self, rosterId, player):
        self.rosters[rosterId].append(player)
        self.freeagents.remove(player)

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        player = next(p for p in self.freeagents if move == p.position)
        rosterId = self.turns.pop(0)
        self.PickFreeAgent(rosterId, player)
        self.playerJustMoved = rosterId

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        pos_max = {"QB": 2, "WR": 6, "RB": 6, "TE": 2, "D": 2, "K": 1,
            "DL": 1, "DB": 1}

        if len(self.turns) == 0: return []

        roster_positions = np.array(
            [p.position for p in self.rosters[self.turns[0]]], dtype=str)
        moves = [pos for pos, max_ in pos_max.items() 
            if np.sum(roster_positions == pos) < max_]
        return moves

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        if playerjm is None: return 0
    
        pos_wgts = {
            ("QB"): [.6, .4],
            ("WR"): [.7, .7, .4, .2],
            ("RB"): [.7, .7, .4, .2],
            ("TE"): [.6, .4],
            ("RB", "WR", "TE"): [.6, .4],
            ("D"): [.6, .3, .1],
            ("K"): [.5, .2, .2, .1]
        }

        result = 0
        # map the drafted players to the weights
        for p in self.rosters[playerjm]:
            max_wgt, _, max_pos, old_wgts = max(
                ((wgts[0], len(lineup_pos), lineup_pos, wgts) 
                    for lineup_pos, wgts in pos_wgts.items()
                    if p.position in lineup_pos),
                default=(0, 0, (), []))
            if max_wgt > 0:
                result += max_wgt * p.points
                old_wgts.pop(0)
                if not old_wgts:
                    pos_wgts.pop(max_pos)
                    
        # map the remaining weights to the top three free agents
        for pos, wgts in pos_wgts.items():
            result += np.mean([p.points for p in self.freeagents 
                if p.position in pos][:3]) * sum(wgts)
            
        return result

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass
