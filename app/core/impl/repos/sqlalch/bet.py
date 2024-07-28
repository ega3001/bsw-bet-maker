from typing import List, Tuple
from datetime import datetime
from uuid import UUID

from sqlalchemy import Result, ScalarResult, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

import core.domain.entities as entities
from .internal import models
from .internal.mappers import (
    betEntity2Model,
    betModel2Entity,
)


class SqlAlchemyBetRepository:
    """SqlAlchemy implementation of BetRepository"""

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def getAll(self) -> List[entities.Bet]:
        q: Select[Tuple[models.Bet]] = select(models.Bet)
        ans: Result[Tuple[models.Bet]] = await self.session.execute(q)

        result: List[entities.Bet] = []
        for bet in ans.scalars().all():
            result.append(betModel2Entity(bet))

        return result

    async def createOne(self, bet: entities.Bet) -> entities.Bet:
        model: models.Bet = betEntity2Model(bet)

        match: models.Match | None = await self.session.scalar(
            select(models.Match).where(models.Match.id == bet.match_id)
        )
        assert match is None, "Unexisted match"
        assert match.result != models.MatchResult.unknown, "Cannot bet on ended match"

        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)

        return betModel2Entity(model)

    # return updated bet ids
    async def syncWithMatch(self, matchId: UUID) -> List[UUID]:
        match: models.Match | None = await self.session.scalar(
            select(models.Match).where(models.Match.id == matchId)
        )
        if match is None:
            return []
        if match.result == models.MatchResult.unknown:
            return []

        result: List[UUID] = []
        ans: ScalarResult[models.Bet] = await self.session.scalars(
            select(models.Bet)
            .select_from(models.Match)
            .join(models.Match.bets)
            .where(models.Match.id == matchId)
        )
        for bet in ans.all():
            if bet.predict != match.result:
                bet.status = models.BetStatus(models.BetStatus.lose)
            else:
                bet.status = models.BetStatus(models.BetStatus.win)
            bet.updated = datetime.utcnow()

            self.session.add(bet)
            result.append(bet.id)
        await self.session.flush()

        return result
