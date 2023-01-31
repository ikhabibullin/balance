import abc

from pydantic import BaseModel, UUID4, PositiveInt


class UserMoney(BaseModel, abc.ABC):
    user_id: UUID4
    money: PositiveInt


class AddMoney(UserMoney):
    pass


class Balance(UserMoney):
    id: UUID4


class ReserveIn(BaseModel):
    user_id: UUID4
    money: PositiveInt
    service_id: UUID4
    order_id: UUID4


class ReserveOut(BaseModel):
    id: UUID4
    balance_id: UUID4
    money: PositiveInt
    service_id: UUID4
    order_id: UUID4

    class Config:
        orm_mode = True
