import uuid
import logging
from enum import IntEnum

from fastapi import (
    APIRouter,
    Depends,
    Body,
    Path,
    BackgroundTasks,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


import core.domain.entities as entities
import core.domain.enums as enums
import core.domain.repos as repos
import core.handlers as handlers
from core.impl.repos.sqlalch import (
    get_db,
    SqlAlchemyBetRepository,
    SqlAlchemyMatchRepository,
)


MatchesRouter = APIRouter(prefix="/events")
logger = logging.getLogger("router-events")


class ResponseOne(BaseModel):
    result: entities.Match


class RequestStatus(IntEnum):
    frstTeamWin = enums.MatchResult.frstTeamWin
    scndTeamWin = enums.MatchResult.scndTeamWin


def getBetRepo(session: AsyncSession = Depends(get_db)) -> SqlAlchemyBetRepository:
    return SqlAlchemyBetRepository(session)


def getMatchRepo(session: AsyncSession = Depends(get_db)) -> SqlAlchemyMatchRepository:
    return SqlAlchemyMatchRepository(session)


@MatchesRouter.put(
    path="/{match_id}",
    tags=["Match", "Put"],
    description="Get all bets.",
    response_model=ResponseOne,
)
async def getAll(
    bkgTasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db),
    matchRepo: repos.MatchRepository = Depends(getMatchRepo),
    betRepo: repos.BetRepository = Depends(getBetRepo),
    match_id: uuid.UUID = Depends(),
    newResult: RequestStatus = Depends(),
) -> ResponseOne:
    match, tasks = await handlers.updateStatus(session, matchRepo, match_id, newResult)
    for task in tasks:
        bkgTasks.add_task(task, session, betRepo)

    return ResponseOne(result=match)
