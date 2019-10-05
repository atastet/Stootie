import datetime
import uuid

from flask import jsonify, abort

from core import segment
from core.mail import send_mail


def _treat_request(body):
    event_name = body.get("type").replace(".", "_")
    user_id = body.get("customer_user_id")
    if event_name is None:
        return [0, body]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    event = {
        "event": event_name,
        "properties": body,
        "timestamp": timestamp
    }
    if user_id is None:
        event["anonymousId"] = uuid.uuid1().hex
    else:
        event["userId"] = user_id
    return [2, event]


def stripe_view(f_request):
    stripe_error_subject = "Stripe Export Error"
    if f_request.method == 'POST':
        body = f_request.json
        event = _treat_request(body) if body else 1

        if event[0] == 0:
            send_mail(body=("Miss event name or user_id %s" % str(event[1])), subject=stripe_error_subject,
                      force_mail=True)
            abort(404)
        elif event[0] == 1:
            send_mail(body="Miss body in request", subject=stripe_error_subject)
            abort(404)
        else:
            send_event = {
                "service": "STRIPE",
                "event": event[1]
            }
            segment.track(send_event)
            response = {
                "response": "Well Done!"
            }
            response = jsonify(response)
            return response
    elif f_request.method == 'GET':
        send_mail(body="GET request instead of POST", subject=stripe_error_subject)
        abort(404)
