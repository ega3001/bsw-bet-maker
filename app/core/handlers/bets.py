from typing import List
from uuid import UUID
from enum import IntEnum
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.entities import Bet
import core.domain.enums as enums
from core.domain.repos import BetRepository
from core.domain.value_objects import Money


class PossibleResults(IntEnum):
    frstTeamWin = enums.MatchResult.frstTeamWin
    scndTeamWin = enums.MatchResult.scndTeamWin


async def getAllBets(session: AsyncSession, betRep: BetRepository) -> List[Bet]:
    async with session.begin() as _:
        return await betRep.getAll()


async def bet(
    session: AsyncSession,
    betRep: BetRepository,
    match_id: UUID,
    predict: PossibleResults,
    amount: Money,
) -> Bet:
    async with session.begin() as s:
        bet = Bet(
            id=UUID(int=0),
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            predict=enums.MatchResult(predict),
            status=enums.BetStatus.unknown,
            amount=amount,
            match_id=match_id,
        )
        bet = await betRep.createOne(bet)
        await s.commit()

    return bet
