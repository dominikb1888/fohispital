import redis
# TODO: Move database connection to other file
r = redis.Redis(host='localhost', port=6379, db=0)


