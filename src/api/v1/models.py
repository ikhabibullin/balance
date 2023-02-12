import abc

from pydantic import BaseModel, PositiveInt, UUID4

from models import StatusEnum


class UserMoney(BaseModel, abc.ABC):
    user_id: UUID4
    money: PositiveInt


class AddMoney(UserMoney):
    pass


class Balance(UserMoney):
    class Config:
        orm_mode = True


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
    status: StatusEnum

    class Config:
        orm_mode = True
