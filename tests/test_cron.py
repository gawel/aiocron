# -*- coding: utf-8 -*-
from aiocron import asyncio
from aiocron import crontab
from aiocron import Cron
import pytest


class CustomError(Exception):
    pass


def test_str():
    loop = asyncio.new_event_loop()

    @crontab('* * * * * *', loop=loop)
    def t():
        pass

    assert '* * * * *' in str(t)


def test_cron():
    loop = asyncio.new_event_loop()

    future = asyncio.Future(loop=loop)

    @crontab('* * * * * *', start=False, loop=loop)
    def t():
        future.set_result(1)

    t.start()
    loop.run_until_complete(future)
    t.stop()
    assert future.result() == 1


def test_raise():
    loop = asyncio.new_event_loop()

    future = asyncio.Future(loop=loop)

    @crontab('* * * * * *', start=False, loop=loop)
    def t():
        loop.call_later(1, future.set_result, 1)
        raise ValueError()

    t.start()
    loop.run_until_complete(future)
    t.stop()
    assert future.result() == 1


def test_next():
    loop = asyncio.new_event_loop()

    def t():
        return 1

    t = crontab('* * * * * *', func=t, loop=loop)

    future = asyncio.async(t.next(), loop=loop)

    loop.run_until_complete(future)
    assert future.result() == 1


def test_null_callback():
    loop = asyncio.new_event_loop()

    t = crontab('* * * * * *', loop=loop)

    assert t.handle is None  # not started

    future = asyncio.async(t.next(4), loop=loop)

    loop.run_until_complete(future)
    assert future.result() == (4,)


def test_next_raise():
    loop = asyncio.new_event_loop()

    @crontab('* * * * * *', loop=loop)
    def t():
        raise CustomError()

    future = asyncio.async(t.next(), loop=loop)

    with pytest.raises(CustomError):
        loop.run_until_complete(future)


def test_coro_next():
    loop = asyncio.new_event_loop()

    @crontab('* * * * * *', loop=loop)
    @asyncio.coroutine
    def t():
        return 1

    future = asyncio.async(t.next(), loop=loop)

    loop.run_until_complete(future)
    assert future.result() == 1


def test_coro_next_raise():
    loop = asyncio.new_event_loop()

    @crontab('* * * * * *', loop=loop)
    @asyncio.coroutine
    def t():
        raise CustomError()

    future = asyncio.async(t.next(), loop=loop)

    with pytest.raises(CustomError):
        loop.run_until_complete(future)
