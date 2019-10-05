from flask import Flask, abort
from flask import request as f_request
from core.appsflyer import appsflyer_view
from core.stripe import stripe_view

app = Flask(__name__)


@app.route('/appsflyer/android', methods=["GET", "POST"])
def appsflyer_android():
    response = appsflyer_view(f_request, "android")
    return response


@app.route('/appsflyer/ios', methods=["GET", "POST"])
def appsflyer_ios():
    response = appsflyer_view(f_request, "ios")
    return response


@app.route('/stripe', methods=["GET", "POST"])
def stripe():
    response = stripe_view(f_request)
    return response


if __name__ == "__main__":
    app.run()
