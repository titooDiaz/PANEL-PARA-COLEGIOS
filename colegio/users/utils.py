import redis

r = redis.Redis()

def is_user_online(user_id):
    return r.exists(f"user_online_{user_id}")