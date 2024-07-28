import core.domain.entities as entities
import core.domain.enums as DEnums
from core.domain.value_objects import Money
from .. import models


def betModel2Entity(model: models.Bet) -> entities.Bet:
    return entities.Bet(
        id=model.id,
        created=model.created,
        updated=model.updated,
        predict=DEnums.MatchResult(model.predict),
        status=DEnums.BetStatus(model.status),
        amount=Money(
            amount=model.amount, Currenncy=DEnums.CurrencyType(model.currency)
        ),
        match_id=model.match_id,
    )


def betEntity2Model(entity: entities.Bet) -> models.Bet:
    return models.Bet(
        id=entity.id,
        created=entity.created,
        updated=entity.updated,
        predict=entity.predict,
        status=entity.status,
        amount=entity.amount.amount,
        currency=entity.amount.Currenncy,
        match_id=entity.match_id,
    )


def matchModel2Entity(model: models.Match) -> entities.Match:
    return entities.Match(
        id=model.id,
        created=model.created,
        updated=model.updated,
        status=DEnums.MatchStatus(model.status),
        result=DEnums.MatchResult(model.result),
    )


def matchEntity2Model(entity: entities.Match) -> models.Match:
    return models.Match(
        id=entity.id,
        created=entity.created,
        updated=entity.updated,
        status=entity.status,
        result=entity.result,
    )
