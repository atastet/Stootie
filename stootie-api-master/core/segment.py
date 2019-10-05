import requests
import os
import json


def track(event):
    service = event["service"]
    key_username = "WRITE_KEY_" + service + "_STOOTIE"
    url = "https://api.segment.io/v1/track"
    username = os.environ[key_username]
    password = ""
    headers = {'Content-Type': 'application/json'}
    event = json.dumps(event["event"])
    response = requests.post(url, headers=headers, auth=(username, password), data=event)
    return response
