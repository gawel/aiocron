# -*- coding: utf-8 -*-
from croniter.croniter import croniter
from datetime import datetime
from tzlocal import get_localzone
from uuid import uuid4
import time
try:
    import asyncio
except ImportError:  # pragma: no cover
    import trollius as asyncio  # NOQA


@asyncio.coroutine
def null_callback(*args):
    return args


def wrap_func(func):
    """wrap in a coroutine"""
    if not asyncio.iscoroutinefunction(func):
        return asyncio.coroutine(func)
    return func


class Cron(object):

    def __init__(self, spec, func=None, start=False, uuid=None, loop=None):
        self.spec = spec
        self.func = func if func is not None else null_callback
        self.cron = wrap_func(self.func)
        self.auto_start = start
        self.uuid = uuid if uuid is not None else uuid4()
        self.handle = self.future = self.croniter = None
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        if start and self.func is not null_callback:
            self.handle = self.loop.call_soon_threadsafe(self.start)

    def start(self):
        """Start scheduling"""
        print('start')
        self.stop()
        self.initialize()
        self.handle = self.loop.call_at(self.get_next(), self.call_next)

    def stop(self):
        """Stop scheduling"""
        if self.handle is not None:
            self.handle.cancel()
        self.handle = self.future = self.croniter = None

    @asyncio.coroutine
    def next(self, *args):
        """yield from .next()"""
        self.initialize()
        self.future = asyncio.Future(loop=self.loop)
        self.handle = self.loop.call_at(self.get_next(), self.call_func, *args)
        return self.future

    def initialize(self):
        """Initialize croniter and related times"""
        if self.croniter is None:
            self.time = time.time()
            self.datetime = datetime.now(get_localzone())
            self.loop_time = self.loop.time()
            self.croniter = croniter(self.spec, start_time=self.datetime)

    def get_next(self):
        """Return next iteration time related to loop time"""
        return self.loop_time + (self.croniter.get_next(float) - self.time)

    def call_next(self):
        """Set next hop in the loop. Call task"""
        if self.handle is not None:
            self.handle.cancel()
        next_time = self.get_next()
        self.handle = self.loop.call_at(next_time, self.call_next)
        self.call_func()

    def call_func(self, *args, **kwargs):
        """Called. Take care of exceptions using gather"""
        asyncio.gather(
            self.cron(*args, **kwargs),
            loop=self.loop, return_exceptions=True
            ).add_done_callback(self.set_result)

    def set_result(self, result):
        """Set future's result if needed (can be an exception).
        Else raise if needed."""
        result = result.result()[0]
        if self.future is not None:
            if isinstance(result, Exception):
                self.future.set_exception(result)
            else:
                self.future.set_result(result)
            self.future = None
        elif isinstance(result, Exception):
            raise result

    def __call__(self, func):
        """Used as a decorator"""
        self.func = func
        self.cron = wrap_func(func)
        if self.auto_start:
            self.loop.call_soon_threadsafe(self.start)
        return self

    def __str__(self):
        return '{0.spec} {0.func}'.format(self)

    def __repr__(self):
        return '<Cron {0.spec} {0.func}>'.format(self)


def crontab(spec, func=None, start=True, loop=None):
    return Cron(spec, func=func, start=start, loop=loop)
