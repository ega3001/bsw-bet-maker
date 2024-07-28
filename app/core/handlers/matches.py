from typing import Tuple, Callable, List, Awaitable
from uuid import UUID
from enum import IntEnum
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.entities import Match
import core.domain.enums as enums
from core.domain.repos import MatchRepository, BetRepository
from core.domain.value_objects import Money


class PossibleResults(IntEnum):
    frstTeamWin = enums.MatchResult.frstTeamWin
    scndTeamWin = enums.MatchResult.scndTeamWin


async def updateStatus(
    session: AsyncSession,
    matchRep: MatchRepository,
    match_id: UUID,
    newResult: PossibleResults,
) -> Tuple[Match, List[Callable[[AsyncSession, BetRepository], Awaitable[None]]]]:

    async def task(session: AsyncSession, betRepo: BetRepository) -> None:
        async with session.begin() as s:
            _: List[UUID] = await betRepo.syncWithMatch(matchId=match_id)
            await s.commit()

    async with session.begin() as s:
        result: Match = await matchRep.updateResult(
            id=match_id, newStatus=enums.MatchResult(value=newResult)
        )
        await s.commit()

    return result, [task]
