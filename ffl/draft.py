from ffl import models

class FreeAgent:
    def __init__(self, id, name, team, positions, points):
        self.espn_id = id
        self.name = name
        self.team = team
        self.positions = positions
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
        rosters = map(lambda r: r[:], self.rosters)
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
        player = next(p for p in self.freeagents if move in p.positions)
        rosterId = self.turns.pop(0)
        self.PickFreeAgent(rosterId, player)
        self.playerJustMoved = rosterId

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        MAX_POS = [("QB", 3), ("WR", 8), ("RB", 8), ("TE", 2), ("EDR", 2),
                ("D", 2), ("K", 2)]

        if len(self.turns) == 0: return []

        roster = self.rosters[self.turns[0]]
        moves = [k for (k, v) in MAX_POS if len([p for p in roster if (k in
            p.positions)]) < v]
        # moves2 = reduce(set.union, [p.positions for p in self.freeagents], set())
        # moves = set(moves).intersection(moves2)
        return list(moves)

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """
        WEIGHTS_POS = [(["QB"], .6),
                       (["WR"], .7),
                       (["WR"], .7),
                       (["RB"], .7),
                       (["RB"], .7),
                       (["TE"], .6),
                       (["RB", "WR", "TE"], .6),
                       (["EDR"], .5),
                       (["D"], .6),
                       (["K"], .5),
                       (["QB"], .4),
                       (["WR"], .4),
                       (["RB"], .4),
                       (["TE"], .4),
                       (["RB", "WR", "TE"], .4),
                       (["EDR"], .2),
                       (["D"], .3),
                       (["K"], .2),
                       (["WR"], .2),
                       (["RB"], .2)]

        if playerjm is None: return 0

        roster = sorted(self.rosters[playerjm], key=lambda p: -p.points)
        res = 0
        for (pos, w) in WEIGHTS_POS:
            p = next((p for p in roster if set(p.positions).intersection(pos)), None)
            if p:
                points = p.points
                roster.remove(p)
            else:
                ps = [p.points for p in self.freeagents if
                        set(p.positions).intersection(pos)]
                if len(ps) > 3: ps = ps[:3]
                points = float(sum(ps)) / max(len(ps), 1)
            res += points * w
        return res

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass
