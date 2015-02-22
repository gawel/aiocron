================================================
aiocron - Crontabs for asyncio
================================================

.. image:: https://travis-ci.org/gawel/aiocron.png?branch=master
  :target: https://travis-ci.org/gawel/aiocron
.. image:: https://pypip.in/v/aiocron/badge.png
   :target: https://crate.io/packages/aiocron/
.. image:: https://pypip.in/d/aiocron/badge.png
   :target: https://crate.io/packages/aiocron/

Source: https://github.com/gawel/aiocron/


Usage
=====

aiocron provide a decorator to run function at time::

    >>> @aiocron.crontab('1 9 * * * *')
    ... @asyncio.coroutine::
    ... def attime():
    ...     print('run')
    >>> asyncio.get_event_loop().run_forever()

You can also use it as an object::

    >>> @aiocron.crontab('1 9 * * * *', start=False)
    ... @asyncio.coroutine::
    ... def attime():
    ...     print('run')
    >>> attime.start()
    >>> asyncio.get_event_loop().run_forever()

Your function still be available at `attime.func`

You can also yield from a crontab. In this case, your coroutine can accept
arguments::

    >>> @aiocron.crontab('1 9 * * * *', start=False)
    ... @asyncio.coroutine::
    ... def attime(i):
    ...     print('run %i' % i)

    >>> @asyncio.coroutine
    ... def once():
    ...     try:
    ...         res = yield from attime.next(1)
    ...     except Exception as e:
    ...         print('It failed (%r)' % e)
    ...     else:
    ...         print(res)
    >>> asyncio.get_event_loop().run_forever()

Notice that unlike standard unix crontab you can specify seconds at the 6th
position.
