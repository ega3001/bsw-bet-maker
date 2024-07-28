from enum import IntEnum


class MatchStatus(IntEnum):
    planned = 0
    ongoing = 1
    finished = 2


class MatchResult(IntEnum):
    unknown = 0
    frstTeamWin = 1
    scndTeamWin = 2


class BetStatus(IntEnum):
    unknown = 0
    win = 1
    lose = 2


class CurrencyType(IntEnum):
    USD = 0
    EUR = 1
