import redis
import config


redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_current_state(user_id):
    try:
        return redis_db.get(user_id).decode('utf-8')
    except KeyError:
        return config.States.PHONEBOOK_START.value

def set_state(user_id, value):
    try:
        redis_db.set(user_id, value)
        return True
    except Exception:
        return False
