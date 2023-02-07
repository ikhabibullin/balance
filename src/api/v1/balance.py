from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models import AddMoney, Balance, ReserveIn, ReserveOut
from db import get_transaction_session

from services import BalanceService

router = APIRouter(prefix='', tags=['api'])


@router.post('/add-money', response_model=Balance, summary='Зачисляет деньги на счет пользователя')
async def add_money_api(data: AddMoney, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session, user_id=data.user_id)
    balance_row = await bs.add_money(money=data.money)
    return Balance(user_id=balance_row.user_id, money=balance_row.money)


@router.post('/reserve', summary='Резервирует деньги пользователя')
async def reserve_money_api(data: ReserveIn, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session, user_id=data.user_id)
    reserve = await bs.reserve_money(money=data.money, service_id=data.service_id, order_id=data.order_id)

    return ReserveOut.from_orm(reserve)
