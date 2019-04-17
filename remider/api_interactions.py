import requests, json
from twilio.rest import Client

from infusionset_reminder.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, from_number, \
    to_numbers, token


def send_message(body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for to_number in to_numbers:
        try:
            client.messages.create(body=body, from_=from_number, to=to_number)
        except:
            pass


def change_config_var(label, new_value):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/vnd.heroku+json; version=3',
               "Authorization": "Bearer {}".format(token)}
    data = {label: new_value}

    requests.patch('https://api.heroku.com/apps/reminder-rekina/config-vars', headers=headers,
                   data=json.dumps(data))
