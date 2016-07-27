import aiohttp
import aiohttp_jinja2

from aiohttp import web

from demo.controllers.users import get_all_users


class ViewsHandlers(object):
    async def users(self, request):
        users = await get_all_users(request.app['engine'])
        return web.json_response(users)

    async def simple_response(self, request):
        return web.Response(body=b'Nothing')

    async def failing(self, request):
        result = 42 / 0
        return web.Response(body=b'OK')

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.tp == aiohttp.MsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    ws.send_str(msg.data)
            elif msg.tp == aiohttp.MsgType.error:
                print('ws connection closed with exception %s' %
                      ws.exception())
        print('ws connection closed')
        return ws

    @aiohttp_jinja2.template('page.html')
    async def page(self, request):
        return {'message': 'Hello web!'}

    def configure(self, app):
        router = app.router
        router.add_route('GET', '/fail', self.failing, name='fail')
        router.add_route('GET', '/ws', self.websocket_handler, name='ws')
        router.add_route('GET', '/simple', self.simple_response, name='simple')
        router.add_route('GET', '/users', self.users, name='users')
        router.add_route('GET', '/page', self.page, name='page')
