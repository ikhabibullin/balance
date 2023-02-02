from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models import AddMoney, Balance, ReserveIn, ReserveOut
from db import get_transaction_session

from services import add_money, reserve_money

router = APIRouter(prefix='', tags=['api'])


@router.post('/add-money', response_model=Balance, summary='Зачисляет деньги на счет пользователя')
async def add_money_api(data: AddMoney, session: AsyncSession = Depends(get_transaction_session)):
    balance_row = await add_money(user_id=data.user_id, money=data.money, session=session)
    return Balance(id=balance_row.id, user_id=balance_row.user_id, money=balance_row.money)


@router.post('/reserve', summary='Резервирует деньги пользователя')
async def reserve_money_api(data: ReserveIn):
    reserve = await reserve_money(data=data)

    return ReserveOut.from_orm(reserve)
