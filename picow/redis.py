from picoredis import Redis
import secrets

def connect():
    try:
        r = Redis(host = secrets.REDIS_HOST, port = secrets.REDIS_PORT)
        
        if len(secrets.REDIS_PASSWORD) > 0:
            if len(secrets.REDIS_USER) > 0:
                r.auth(secrets.REDIS_USER, secrets.REDIS_PASSWORD)
            else:
                r.auth(secrets.REDIS_PASSWORD)
                                
        return r
    except OSError as e:
        print("crap")
        print(e)
        return None