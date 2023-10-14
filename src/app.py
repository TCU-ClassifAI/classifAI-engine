from flask import Flask


import os


app = Flask(__name__)

if os.environ.get("ENV") == "production":
    from settings import production as config
else:
    from settings import development as config


# Define routes
@app.route("/")
def index():
    return str(config.meow)


# @app.route("/transcription")
# def service1():
#     result = transcription()
#     return f"Service 1: {result}"


if __name__ == "__main__":
    local = True

    app.run(debug=True)
