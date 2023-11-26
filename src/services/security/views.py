# from flask import Blueprint, request, make_response, jsonify, redirect


# app = Blueprint("profile", __name__)


# # @app.route("/help", methods=["GET"])
# # def help():
# #     """Forwards to the documentation page (https://tcu-classifai.github.io/classifAI-engine/)"""

# #     return redirect("https://tcu-classifai.github.io/classifAI-engine/", code=302)


# # @app.route("/", methods=["GET"])
# # def index():
# #     """Gives a brief description of the API, version, config, and healthcheck. Welcome page"""

# #     description = "ClassifAI Engine"
# #     version = "1.0.0"
# #     config = settings.SETTINGS_TYPE
# #     healthcheck = "OK"
# #     documentation = "https://tcu-classifai.github.io/classifAI-engine/"

# #     return "<h1>{}</h1><p>Version: {}</p><p>Config: {}</p><p>Healthcheck: {}</p><a href='{}'>Documentation</a>".format(
# #         description, version, config, healthcheck, documentation
# #     )


# # @app.route("/healthcheck", methods=["GET"])
# # def healthcheck():
# #     return make_response("OK", 200)


# # @app.route("/config", methods=["GET"])
# # def config():
# #     return make_response(str(settings.SETTINGS_TYPE), 200)
