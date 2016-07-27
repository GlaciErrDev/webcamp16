import asyncio

import pytest
import aiohttp

from aiohttp import web
from demo.handlers import ViewsHandlers


def test_simple_response(loop):
    async def go():
        app = web.Application(loop=loop)
        handler = app.make_handler()
        server = await loop.create_server(handler, '127.0.0.1', 7654)

        with aiohttp.ClientSession(loop=loop) as client:
            handlers = ViewsHandlers()
            handlers.configure(app)
            resp = await client.get('http://127.0.0.1:7654/simple')
            text = await resp.text()
            assert resp.status == 200
            assert text == 'Nothing'
            await resp.release()

        await handler.finish_connections()
        server.close()
        await server.wait_closed()

    loop.run_until_complete(go())


def test_simple_coroutine(loop):
    async def my_coroutine():
        await asyncio.sleep(0.1, loop=loop)
        return 23

    result = loop.run_until_complete(my_coroutine())
    assert result == 23


@pytest.mark.run_loop
async def test_simple_response_with_fixture(loop, create_server):
    app, url = await create_server()
    with aiohttp.ClientSession(loop=loop) as client:
        handlers = ViewsHandlers()
        handlers.configure(app)
        resp = await client.get('{url}/simple'.format(url=url))
        assert resp.status == 200
        await resp.release()
