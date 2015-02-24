# -*- coding: utf-8 -*-
import threading
import asyncio
import aiocron
import time


class CronThread(threading.Thread):

    def __init__(self):
        super(CronThread, self).__init__()
        self.start()
        time.sleep(.1)

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        self.loop.close()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.join()

    def crontab(self, *args, **kwargs):
        kwargs['loop'] = self.loop
        return aiocron.crontab(*args, **kwargs)

cron = CronThread()


@cron.crontab('* * * * * *')
@asyncio.coroutine
def run():
    yield from asyncio.sleep(.1)
    print('It works')

asyncio.get_event_loop().run_forever()
cron.stop()
