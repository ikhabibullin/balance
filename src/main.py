from fastapi import FastAPI

from db import engine, Base

from api.v1.balance import balance_router, reserved_router

app = FastAPI(title='Balance service')
app.include_router(balance_router)
app.include_router(reserved_router)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
