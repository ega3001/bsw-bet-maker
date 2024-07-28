from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import ENUM

from core.domain.enums import MatchResult, MatchStatus, BetStatus, CurrencyType


BaseModel = so.declarative_base()


# TODO: add more constrains


class Bet(BaseModel):
    __tablename__: str = "bets"

    id: so.Mapped[UUID] = so.mapped_column(sa.UUID, primary_key=True, default=uuid4)
    created: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    updated: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    predict: so.Mapped[MatchResult] = so.mapped_column(
        ENUM(MatchResult), nullable=False
    )
    status: so.Mapped[BetStatus] = so.mapped_column(ENUM(BetStatus), nullable=False)
    amount: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)  # ?
    currency: so.Mapped[CurrencyType] = so.mapped_column(
        ENUM(CurrencyType), nullable=False
    )

    match_id: so.Mapped[UUID] = so.mapped_column(
        sa.ForeignKey("matches.id"), nullable=False
    )

    match: so.WriteOnlyMapped[Optional["Match"]] = so.relationship(
        back_populates="bets"
    )


class Match(BaseModel):
    __tablename__: str = "matches"

    id: so.Mapped[UUID] = so.mapped_column(sa.UUID, primary_key=True, default=uuid4)
    created: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    updated: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    status: so.Mapped[MatchStatus] = so.mapped_column(ENUM(MatchStatus), nullable=False)
    result: so.Mapped[MatchResult] = so.mapped_column(ENUM(MatchResult), nullable=False)

    bets: so.WriteOnlyMapped[Optional[List["Bet"]]] = so.relationship(
        back_populates="match"
    )
