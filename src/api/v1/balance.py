from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models import AddMoney, Balance, ReserveIn, ReserveOut
from db import get_transaction_session

from services import BalanceService

balance_router = APIRouter(prefix='', tags=['balance'])
reserved_router = APIRouter(prefix='/reserves', tags=['reserved'])


@balance_router.get('/{user_id}', response_model=Balance, summary='Возвращает баланс пользователя')
async def get_balance_api(user_id: UUID4, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session, user_id=user_id)
    balance = await bs.get_balance()
    if not balance:
        raise HTTPException(
            status_code=404,
            detail='Balance пользователя не найден',
        )
    return Balance.from_orm(balance)


@balance_router.post('/add-money', response_model=Balance, summary='Зачисляет деньги на счет пользователя')
async def add_money_api(data: AddMoney, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session, user_id=data.user_id)
    balance_row = await bs.add_money(money=data.money)
    return Balance(user_id=balance_row.user_id, money=balance_row.money)


@reserved_router.post('', response_model=ReserveOut, summary='Резервирует деньги пользователя')
async def reserve_money_api(data: ReserveIn, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session, user_id=data.user_id)
    reserve = await bs.reserve_money(money=data.money, service_id=data.service_id, order_id=data.order_id)

    return ReserveOut.from_orm(reserve)


@reserved_router.post('/{reserved_id}/reject', summary='Отклоняет принятие зарезервированных денег')
async def reject_reserved_money_api(reserved_id: UUID4, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session)
    reserved = await bs.reject_reserved(reserved_id=reserved_id)

    if not reserved:
        raise HTTPException(status_code=404, detail='Не найден или не в статусе pending')

    return ReserveOut.from_orm(reserved)


@reserved_router.post('/{reserved_id}/accept', summary='Подтверждает принятие зарезервированных денег')
async def accept_reserved_money_api(reserved_id: UUID4, session: AsyncSession = Depends(get_transaction_session)):
    bs = BalanceService(session=session)
    reserved = await bs.accept_reserved(reserved_id=reserved_id)

    if not reserved:
        raise HTTPException(status_code=404, detail='Не найден или не в статусе pending')

    return ReserveOut.from_orm(reserved)
