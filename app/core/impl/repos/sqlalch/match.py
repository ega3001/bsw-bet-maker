from typing import List, Tuple
from uuid import UUID

from sqlalchemy import Result, Select
from sqlalchemy.sql import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningUpdate

# from sqlalchemy.future import select

import core.domain.entities as entities
import core.domain.enums as enums
from .internal import models
from .internal.mappers import (
    matchEntity2Model,
    matchModel2Entity,
)


class SqlAlchemyMatchRepository:
    """SqlAlchemy implementation of MatchRepository"""

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def updateResult(
        self, id: UUID, newStatus: enums.MatchResult
    ) -> entities.Match:
        q: ReturningUpdate[Tuple[models.Match]] = (
            update(models.Match)
            .where(models.Match.id == id)
            .values(status=newStatus)
            .returning(models.Match)
        )
        ans: Result[Tuple[models.Match]] = await self.session.execute(q)
        return matchModel2Entity(ans.scalar_one())
