import asyncio

import sqlalchemy as sa

from aiohttp_security.abc import AbstractAuthorizationPolicy

from demo import db


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, dbengine):
        self.dbengine = dbengine

    @asyncio.coroutine
    def authorized_userid(self, identity):
        with (yield from self.dbengine) as conn:
            where = [db.users.c.login == identity,
                     not db.users.c.disabled]
            query = db.users.count().where(sa.and_(*where))
            ret = yield from conn.scalar(query)
            if ret:
                return identity
            else:
                return None

    @asyncio.coroutine
    def permits(self, identity, permission, context=None):
        # import pdb; pdb.set_trace()
        with (yield from self.dbengine) as conn:
            import pdb; pdb.set_trace()

            query = db.users.select()
            ret = yield from conn.scalar(query)
            if ret is not None:
                if permission in ret:
                    return True
            return False
