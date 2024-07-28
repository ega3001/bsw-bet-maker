from typing import Protocol, List
from uuid import UUID

from .entities import Bet, Match
from .enums import MatchResult


class BetRepository(Protocol):
    async def getAll(self) -> List[Bet]: ...

    async def createOne(self, bet: Bet) -> Bet: ...

    async def syncWithMatch(self, matchId: UUID) -> List[UUID]: ...


class MatchRepository(Protocol):
    async def updateResult(self, id: UUID, newStatus: MatchResult) -> Match: ...
