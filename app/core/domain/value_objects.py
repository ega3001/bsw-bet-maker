from pydantic import BaseModel

from .enums import CurrencyType


class Money(BaseModel):
    amount: int
    Currenncy: CurrencyType
