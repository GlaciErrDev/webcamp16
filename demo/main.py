import asyncio
import pathlib

import jinja2
import aiohttp_admin

from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from aiohttp_debugtoolbar import setup as setup_debugtoolbar
from aiohttp_jinja2 import setup as setup_jinja2
from aiohttp_admin.backends.sa import PGResource
from aiopg.sa import create_engine
from aioredis import create_pool

from demo.db_auth import DBAuthorizationPolicy
from demo.handlers import AuthHandlers, ViewsHandlers
from demo import db, settings


PROJ_ROOT = pathlib.Path(__file__).parent


async def init(loop):
    redis_pool = await create_pool(('localhost', 6379))
    db_engine = await create_engine(user=settings.DB_USER,
                                    password=settings.DB_PASSWORD,
                                    database=settings.DATABASE,
                                    host=settings.DB_HOST)
    app = web.Application(loop=loop)
    app['engine'] = db_engine
    setup_debugtoolbar(app)
    setup_session(app, RedisStorage(redis_pool))
    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(db_engine))
    setup_jinja2(app, loader=jinja2.FileSystemLoader('demo/templates'))

    auth_handlers = AuthHandlers()
    auth_handlers.configure(app)
    if settings.DEBUG:
        app.router.add_static('/static', path=str(PROJ_ROOT / 'static'))
    view_handlers = ViewsHandlers()
    view_handlers.configure(app)
    admin_config = str(PROJ_ROOT / 'static' / 'js')
    setup_admin(app, db_engine, admin_config)
    return app


def setup_admin(app, pg_engine, admin_config_path):
    admin = aiohttp_admin.setup(app, admin_config_path)

    admin.add_resource(PGResource(pg_engine, db.users, url='users'))
    admin.add_resource(PGResource(pg_engine, db.permissions, url='permissions'))
    return admin

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
