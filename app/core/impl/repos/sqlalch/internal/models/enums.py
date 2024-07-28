from sqlalchemy.dialects.postgresql import ENUM


class MatchStatus(ENUM):
    planned = 0
    ongoing = 1
    finished = 2


class MatchResult(ENUM):
    unknown = 0
    frstTeamWin = 1
    scndTeamWin = 2


class BetStatus(ENUM):
    unknown = 0
    win = 1
    lose = 2


class CurrencyType(ENUM):
    USD = 0
    EUR = 1
