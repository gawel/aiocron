# -*- coding: utf-8 -*-
from aiocron import crontab
from aiocron import asyncio
import logging

logging.basicConfig()

loop = asyncio.get_event_loop()


@crontab('* * * * * */3')
def mycron():
    print('function')


@crontab('* * * * * */2', start=False)
def mycron2(i):
    if i == 2:
        raise ValueError(i)
    return 'yielded function (%i)' % i


@asyncio.coroutine
def main():
    cron = crontab('* * * * * */2')
    for i in range(3):
        try:
            yield from cron.next()
        except Exception:
            pass
        else:
            print('yielded (%i)' % i)

    for i in range(3):
        try:
            res = yield from mycron2.next(i)
        except Exception as e:
            print(repr(e))
        else:
            print(res)


loop.run_until_complete(main())

"""
Will print:

    yielded (0)
    function
    yielded (1)
    yielded (2)
    function
    yielded function (0)
    function
    yielded function (1)
    yielded function (2)
"""
