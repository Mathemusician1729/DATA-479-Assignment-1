from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    # Example of reading an environment variable
    user = os.getenv('USER_NAME', 'Student')
    return f"Hello {user}, welcome to Docker!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)