import json
import decimal
import asyncio

import asyncio_redis
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def push(session, url):
    async with session.get(url) as response:
        return await response.text()


@asyncio.coroutine
async def subscribe():
    # Create connection
    # TODO: Add timeout to connection
    connection = await asyncio_redis.Connection.create(host='127.0.0.1', port=6379)

    subscriber = await connection.start_subscribe()
    await subscriber.subscribe(['irage'])
    
    while True:
        await subscriber.next_published()
        # Assuming we got data from data manager. Assuming average comp price is 10. 
        avg_comp_price = 10
        async with aiohttp.ClientSession() as session:
            response = push(session, 'http://localhost:8000/register-request')
            try:
                # TODO: Check for http response.
                response = json.loads(response)
            except:
                print("Invalid response returned from register request api")
            else:
                print("Response %s" % response)

                  
        async with aiohttp.ClientSession() as session:
            # As I used UUID even odd is not possible so taking dummy value 10.
            response = fetch(session, 'http://localhost:8000/request-data/10')
            try:
                # TODO: Check for http response.
                response = json.loads(response)
            except:
                print("Invalid response returned from register request api")
            else:
                if response.get('sale') == True:
                    print(decimal.Decimal(avg_comp_price) * decimal.Decimal(1.1))
                elif response.get('sale') == False:
                    print(decimal.Decimal(avg_comp_price) * decimal.Decimal(0.9))

loop = asyncio.get_event_loop()
asyncio.ensure_future(subscribe())
loop.run_forever()
loop.close()
