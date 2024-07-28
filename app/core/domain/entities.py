from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from .enums import MatchStatus, BetStatus, MatchResult
from .value_objects import Money


# TODO: add immutable fields


class Match(BaseModel):
    id: UUID
    created: datetime
    updated: datetime
    status: MatchStatus
    result: MatchResult


class Bet(BaseModel):
    id: UUID
    created: datetime
    updated: datetime
    predict: MatchResult
    status: BetStatus
    amount: Money
    match_id: UUID
