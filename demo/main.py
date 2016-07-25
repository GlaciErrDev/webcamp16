import asyncio

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiopg.sa import create_engine
from aioredis import create_pool

from demo.db_auth import DBAuthorizationPolicy
from demo.handlers import Web
from demo import settings


async def init(loop):
    redis_pool = await create_pool(('localhost', 6379))
    dbengine = await create_engine(user=settings.DB_USER,
                                   password=settings.DB_PASSWORD,
                                   database=settings.DATABASE,
                                   host=settings.DB_HOST)
    app = web.Application(loop=loop)
    setup_session(app, RedisStorage(redis_pool))
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(dbengine))

    web_handlers = Web()
    web_handlers.configure(app)

    return app


# todo (misha): add finilizer
async def finalize(srv, app, handler):
    sock = srv.sockets[0]
    app.loop.remove_reader(sock.fileno())
    sock.close()

    await handler.finish_connections(1.0)
    srv.close()
    await srv.wait_closed()
    await app.finish()


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app, host=settings.RUN_HOST, port=settings.RUN_PORT)


if __name__ == '__main__':
    main()
