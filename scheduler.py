import asyncio

import asyncio_redis


@asyncio.coroutine
def publish():
    # Create connection
    # TODO: Add timeout to connection
    connection = yield from asyncio_redis.Connection.create(host='127.0.0.1', port=6379)

    try:
        yield from connection.publish('irage', 'Event')
    except asyncio_redis.Error as e:
        print('Published failed', repr(e))
    else:
        print('Published')


@asyncio.coroutine
def event():
    while True:
        yield from asyncio.sleep(5)
        # This might be not acurate if publish takes more time. 
        # We can have async Queue to optimise further.
        yield from publish()


loop = asyncio.get_event_loop()
asyncio.ensure_future(event())
loop.run_forever()
loop.close()
