# -*- coding: utf-8 -*-
from croniter.croniter import croniter
from uuid import uuid4
import logging
import time
try:
    import asyncio
except ImportError:  # pragma: no cover
    import trollius as asyncio  # NOQA

log = logging.getLogger(__name__)


@asyncio.coroutine
def null_callback():  # pragma: no cover
    pass


def wrap_func(func):
    if func is None:
        func = null_callback
    if not asyncio.iscoroutinefunction(func):
        return asyncio.coroutine(func)
    return func


class Cron(object):

    def __init__(self, spec, func, start=False, uuid=None, loop=None):
        self.spec = spec
        self.func = self.cron = func
        self.cron = wrap_func(func)

        if loop is None:  # pragma: no cover
            loop = asyncio.get_event_loop()
        self.loop = loop

        if uuid is None:
            uuid = uuid4
        self.uuid = uuid

        self.auto_start = start

        self.handle = self.future = self.croniter = None

    def initialize(self):
        if not self.croniter:
            self.time = time.time()
            self.loop_time = self.loop.time()
            self.croniter = croniter(self.spec, start_time=self.time)

    def get_next(self):
        return self.loop_time + (self.croniter.get_next(float) - self.time)

    def start(self):
        self.stop()
        self.initialize()
        self.handle = self.loop.call_at(self.get_next(), self.call_next)

    def stop(self):
        if self.handle:
            self.handle.cancel()
        self.handle = None
        self.croniter = None

    def call_next(self):
        if self.handle:
            self.handle.cancel()
        next_time = self.get_next()
        self.handle = self.loop.call_at(next_time, self.call_next)
        self.call_func()

    def call_func(self, *args, **kwargs):
        task = asyncio.gather(self.cron(*args, **kwargs),
                              loop=self.loop,
                              return_exceptions=True)
        task.add_done_callback(self.set_result)

    def set_result(self, result):
        result = result.result()[0]
        if self.future is not None:
            if isinstance(result, Exception):
                self.future.set_exception(result)
            else:
                self.future.set_result(result)
            self.future = None
        elif isinstance(result, Exception):
            self.future = None
            raise result

    @asyncio.coroutine
    def next(self, *args):
        self.initialize()
        self.future = asyncio.Future(loop=self.loop)
        self.handle = self.loop.call_at(self.get_next(), self.call_func, *args)
        return self.future

    def __call__(self, func):
        self.func = self.cron = func
        self.cron = wrap_func(func)
        if self.auto_start:
            self.start()
        return self

    def __str__(self):
        return '{0.spec} {0.func}'.format(self)

    def __repr__(self):
        return '<Cron %s>' % self


def crontab(spec, start=True, loop=None):
    return Cron(spec, func=None, start=start, loop=loop)
