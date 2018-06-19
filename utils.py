import time

import time_uuid


def generate_uuid():
    current_timestamp = time.time()
    return time_uuid.TimeUUID.with_timestamp(current_timestamp)
   

def get_timestamp_from_uuid(uuid):
    try:
        uuid_instance = time_uuid.TimeUUID(uuid)
    except ValueError:
        return None
    else:
        return uuid_instance.get_datetime()
 
