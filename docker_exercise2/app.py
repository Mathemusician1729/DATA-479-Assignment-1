from flask import Flask
from redis import Redis

app = Flask(__name__)
# Notice host is 'redis' (the service name in docker-compose), not 'localhost' or an IP!
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    count = redis.incr('hits')
    return f"Hello! You have viewed this page {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)