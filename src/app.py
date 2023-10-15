from flask import Flask, request, make_response
from services.transcription import transcribe


# import os


app = Flask(__name__)

# if os.environ.get("ENV") == "production":
#     from settings import production as config
# else:
#     from settings import development as config


# Define routes
@app.route("/")
def index():
    return make_response("Hello, world!", 200)


@app.route("/transcription", methods=["GET", "POST"])
def get_transcription():
    # Get the query parameters
    path = request.args.get("path", default=None)

    try:
        result = transcribe(path)
        return make_response(result, 200)
    except Exception as e:
        return make_response(str(e), 500)


if __name__ == "__main__":
    local = True

    app.run(debug=True)
