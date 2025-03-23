================================================
aiocron - Crontabs for asyncio
================================================


.. image:: https://img.shields.io/pypi/v/aiocron.svg
  :target: https://pypi.python.org/pypi/aiocron
.. image:: https://img.shields.io/pypi/dm/aiocron.svg
  :target: https://pypi.python.org/pypi/aiocron

Usage
=====

``aiocron`` provide a decorator to run function at time::

    >>> import aiocron
    >>> import asyncio
    >>>
    >>> @aiocron.crontab('*/30 * * * *')
    ... async def attime():
    ...     print('run')
    ...
    >>> asyncio.get_event_loop().run_forever()

You can also use it as an object::

    >>> @aiocron.crontab('1 9 * * 1-5', start=False)
    ... async def attime():
    ...     print('run')
    ...
    >>> attime.start()
    >>> asyncio.get_event_loop().run_forever()

Your function still be available at ``attime.func``

You can also await a crontab. In this case, your coroutine can accept
arguments::

    >>> @aiocron.crontab('0 9,10 * * * mon,fri', start=False)
    ... async def attime(i):
    ...     print('run %i' % i)
    ...
    >>> async def once():
    ...     try:
    ...         res = await attime.next(1)
    ...     except Exception as e:
    ...         print('It failed (%r)' % e)
    ...     else:
    ...         print(res)
    ...
    >>> asyncio.get_event_loop().run_forever()

Finally you can use it as a sleep coroutine. The following will wait until
next hour::

    >>> await crontab('0 * * * *').next()

If you don't like the decorator magic you can set the function by yourself::

    >>> cron = crontab('0 * * * *', func=yourcoroutine, start=False)

``aiocron`` use `cronsim <https://github.com/cuu508/cronsim>`_. Refer to
it's documentation to know more about crontab format.

From Dec 31, 2024, ``aiocron`` has switched from ``croniter`` to ``cronsim``
for cron expression parsing (`PR #39 <https://github.com/gawel/aiocron/pull/39>`_). 
Please ensure that your cron expressions are valid in ``cronsim``. For a comparison of 
features between ``croniter`` and ``cronsim``, refer to 
`cronsim documentation <https://github.com/cuu508/cronsim?tab=readme-ov-file#cron-expression-feature-matrix>`_.
