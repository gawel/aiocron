# -*- coding: utf-8 -*-
from aiocron import crontab
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@crontab("* * * * * */3", loop=loop)
def mycron():
    print("function")

@crontab("* * * * * */2", start=False, loop=loop)
def mycron2(i):
    if i == 2:
        raise ValueError(i)
    return f"yielded function ({i})"

async def main():
    cron = crontab("* * * * * */2", loop=loop)
    for i in range(3):
        try:
            await cron.next()
        except Exception:
            pass
        else:
            print(f"yielded ({i})")

    for i in range(3):
        try:
            res = await mycron2.next(i)
        except Exception as e:
            print(repr(e))
        else:
            print(res)

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

"""
Expected output (may vary slightly due to timing):

    yielded (0)
    function
    yielded (1)
    yielded (2)
    function
    yielded function (0)
    function
    yielded function (1)
    ValueError(2)
"""