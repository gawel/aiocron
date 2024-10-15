# -*- coding: utf-8 -*-
import threading
import asyncio
import aiocron
import time


class CronThread(threading.Thread):
    def __init__(self):
        super(CronThread, self).__init__()
        self.loop = None
        self.start()
        time.sleep(0.1)  # Give time for the loop to start

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.join()
            self.loop.close()

    def crontab(self, *args, **kwargs):
        kwargs["loop"] = self.loop
        return aiocron.crontab(*args, **kwargs)


cron = CronThread()


@cron.crontab("* * * * * *")
async def run():
    await asyncio.sleep(0.1)
    print("It works")


# Run for a short time then stop
try:
    time.sleep(5)  # Let it run for 5 seconds
finally:
    cron.stop()
    print("Cron stopped")