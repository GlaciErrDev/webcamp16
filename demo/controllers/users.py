from demo.db import users


async def get_all_users(engine):
    result = []
    async with engine.acquire() as conn:
        async for row in conn.execute(users.select().where(~users.c.disabled)):
            print(row.login, row.password)
            result.append(row.login)
    return result


