import enum
import uuid

from pydantic import UUID4
from sqlalchemy import Column, CheckConstraint, Integer, ForeignKey, DateTime, func, Enum, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class TimeStampedMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StatusEnum(str, enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class Balance(Base, TimeStampedMixin):
    __tablename__ = 'balance'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    money = Column(Integer, default=0, nullable=False)
    reserved = relationship('Reserved')

    __table_args__ = (CheckConstraint(money >= 0, name='balance_money_positive_constraint'),)

    @classmethod
    def returning(cls):
        return [cls.user_id, cls.money]


class Reserved(Base, TimeStampedMixin):
    __tablename__ = 'reserved'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance_id = Column(UUID(as_uuid=True), ForeignKey('balance.user_id'), nullable=False)
    money = Column(Integer, nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (CheckConstraint(money >= 0, name='reserved_money_positive_constraint'),)

    @classmethod
    def returning(cls):
        return [cls.id, cls.balance_id, cls.money, cls.service_id, cls.order_id, cls.status]

    @classmethod
    def get_update_stmt(cls, reserved_id: UUID4, values: dict):
        stmt = (
            update(cls)
            .filter(cls.id == reserved_id, cls.status == StatusEnum.pending)
            .values(values)
            .returning(*cls.returning())
        )
        return stmt
