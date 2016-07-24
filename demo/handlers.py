import asyncio
import functools

from aiohttp import web


from aiohttp_security import remember, forget, authorized_userid, permits


def require(permission):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(self, request):
            has_perm = yield from permits(request, permission)
            if not has_perm:
                raise web.HTTPForbidden()
            return (yield from f(self, request))
        return wrapped
    return wrapper


class Web(object):
    @require('public')
    def index(self, request):
        pass

    @require('public')
    def login(self, request):
        pass

    @require('protected')
    def logout(self, request):
        pass

    @require('public')
    def public(self, request):
        pass

    @require('protected')
    def protected(self, request):
        pass

    def configure(self, app):
        router = app.router
        router.add_route('GET', '/', self.index, name='index')
        router.add_route('POST', '/login', self.login, name='login')
        router.add_route('POST', '/logout', self.logout, name='logout')
        router.add_route('GET', '/public', self.public, name='public')
        router.add_route('GET', '/protected', self.protected, name='protected')
