from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis-service', port=6379)

@app.route('/')
def hello_world():
    redis.incr('hits')
    page_count = redis.get('hits').decode('utf-8')  # Convert bytes to string
    return f'KEEP LEARNING, KEEP MOVING AHEAD Page_Count {page_count}'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
