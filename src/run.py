from flask import Flask, make_response

# from services.transcription import transcribe, start_transcription, check_transcription

from transcription.profile import profile
from transcription.views import transcription


app = Flask(__name__)
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(transcription, url_prefix="/transcription")


# if os.environ.get("ENV") == "production":
#     from settings import production as config
# else:
#     from settings import development as config


# @app.route("/start_transcription", methods=["POST"])
# def start_transcription_endpoint():
#     # Check if the file was uploaded
#     if "file" not in request.files:
#         return make_response("No file uploaded", 400)

#     file = request.files["file"]

#     # print the file name
#     print(file.filename)

#     model_type = (
#         request.form["model_type"]
#         if "model_type" in request.form
#         else config.MODEL_TYPE
#     )

#     job_id = start_transcription(file, model_type)

#     return make_response(job_id, 200)


# @app.route("/get_transcription", methods=["GET"])
# def get_transcription_endpoint():
#     # Get the query parameters
#     job_id = request.form.get("job_id", default=None)

#     print(job_id)

#     try:
#         result = check_transcription(job_id)
#         return make_response(result, 200)
#     except Exception as e:
#         return make_response(str(e), 500)


# @app.route("/transcription", methods=["GET", "POST"])
# def get_transcription():
#     # Get the query parameters
#     path = request.args.get("path", default=None)

#     try:
#         result = transcribe(path)
#         return make_response(result, 200)
#     except Exception as e:
#         return make_response(str(e), 500)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return make_response("OK", 200)


@app.errorhandler(404)
def not_found(error):
    return make_response("Route not found", 404)


if __name__ == "__main__":
    local = True

    app.run(debug=True)
