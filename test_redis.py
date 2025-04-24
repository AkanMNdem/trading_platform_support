import redis

# Connect to local Redis server
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Test set and get
r.set('test', 'value')
print(r.get('test'))  # Expected output: b'value'
