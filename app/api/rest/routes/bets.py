import uuid
import logging
from dataclasses import dataclass
from enum import IntEnum
from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


import core.domain.entities as entities
import core.domain.enums as enums
import core.domain.repos as repos
import core.domain.value_objects as vals
import core.handlers as handlers
from core.impl.repos.sqlalch import (
    get_db,
    SqlAlchemyBetRepository,
    SqlAlchemyMatchRepository,
)


BetsRouter = APIRouter(prefix="/bets")
logger = logging.getLogger("router-bets")


class ResponseList(BaseModel):
    result: List[entities.Bet]


class ResponseOne(BaseModel):
    result: entities.Bet


class RequestPredict(IntEnum):
    frstTeamWin = enums.MatchResult.frstTeamWin
    scndTeamWin = enums.MatchResult.scndTeamWin


class RequestCreate(BaseModel):
    match_id: uuid.UUID
    predict: RequestPredict
    amount: vals.Money


@dataclass
class RequestContext:
    session: AsyncSession | None = None
    betRepo: repos.BetRepository | None = None
    matchRepo: repos.MatchRepository | None = None


def prepareSession(session: AsyncSession = Depends(get_db)) -> RequestContext:
    return RequestContext(session=session)


def prepareBetRepo(session: AsyncSession = Depends(get_db)) -> RequestContext:
    return RequestContext(session=session, betRepo=SqlAlchemyBetRepository(session))


def prepareBetMatchRepo(session: AsyncSession = Depends(get_db)) -> RequestContext:
    return RequestContext(
        session=session,
        betRepo=SqlAlchemyBetRepository(session),
        matchRepo=SqlAlchemyMatchRepository(session),
    )


@BetsRouter.get(
    path="/",
    tags=["Bet", "Get"],
    description="Get all bets.",
    response_model=ResponseList,
)
async def getAll(
    session: AsyncSession = Depends(get_db),
    context: RequestContext = Depends(prepareBetRepo),
) -> ResponseList:
    bets: List[entities.Bet] = await handlers.getAllBets(
        context.session, context.betRepo
    )
    return ResponseList(result=bets)


@BetsRouter.post(
    path="/",
    tags=["Bet", "Post"],
    description="Create new bet",
    response_model=ResponseOne,
)
async def createOne(
    request: RequestCreate = Depends(),
    context: RequestContext = Depends(prepareBetRepo),
) -> ResponseOne:
    bet = await handlers.bet(
        context.session,
        context.betRepo,
        request.match_id,
        request.predict,
        request.amount,
    )
    return ResponseOne(result=bet)
