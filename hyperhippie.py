import os
import sys
import json
from datetime import datetime

from metros import  *
import requests
from flask import Flask, request

app = Flask(__name__)


VERIFY_TOKEN=''
PAGE_ACCESS_TOKEN = ''
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    print (message_text)
                    print type(message_text)
                    message_text = str(message_text)

                    if message_text.lower().startswith( "hi") or message_text.lower().startswith( "hello") :
                        print (message_text)
                        send_message(sender_id, "Hello, Traveller!")
                        send_message(sender_id, "To know about monuments near metro stations please type:")
                        send_message(sender_id, "monuments near <Metro Station Name>")
                    elif message_text.lower().startswith("monuments near"):
                        send_monuments_list(sender_id,message_text)
                    else:
                        send_message(sender_id, "I did not understand your message :( ")
                        #send_metros_list(recipient_id)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200





if __name__ == '__main__':
    app.run(debug=True)
