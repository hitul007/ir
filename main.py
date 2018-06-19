import time

import utils as main_utils
import db_utils

from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route('/register-request', methods=["POST"])
async def register_request(request):
    # Generate UUID
    uuid = main_utils.generate_uuid()

    # Store UUID into mongodb
    mongo_instance = db_utils.MongoDB()
    mongo_db_instance = mongo_instance.get_instance()

    await db_utils.insert_uuid(mongo_db_instance, uuid)
    
    return json({'id': str(uuid)})


@app.route('/register-request/<id>')
async def request_data(request, id):
    sale = False
    if not id.isdigit():
        return json({'sale': False})

    id = int(id)
    if id % 2 == 0:
        return json({'sale': True})
    else:
        return json({'sale': False})

    return json({'sale': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

