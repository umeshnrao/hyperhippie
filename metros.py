import sys
import json
from datetime import datetime
from difflib import SequenceMatcher
from fuzzywuzzy import process

import requests
import re
PAGE_ACCESS_TOKEN = ''


def remove_non_ascii(text):
    return "".join(filter(lambda x: ord(x) < 128, text))




def test_msg(recipient_id):
    data = json.load(open(r'C:\Users\unrao\Desktop\template_sample.json'))

    data["recipient"]['id']=recipient_id
    print(data)

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text='template'))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps(data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)




def send_monuments_list(recipient_id,message_text):
    metros = ['Netaji Subhash Place Metro Station', 'Rajiv Chowk Metro Station ', 'Central Secretariat Metro Station',
              'Chandni Chowk Metro Station', 'Qutab Minar Metro Station', 'Jor Bagh Minar Metro Station',
              'Patel Chowk Metro Station', 'Hauz Khas Metro Station', 'Akshardham Temple Metro Station',
              'Pragati Maidan Metro Station', 'Rajouri Garden Metro Station', 'Karol Bagh Metro Station',
              'Jangpura Metro Station', 'Nehru Place Metro Station', 'Tughlaqabad Metro Station']
    message_text = message_text.lower()
    match = re.search('monuments near ([a-z ]*)', message_text )
    if match != None:
        my_metro =  (match.group(1))
    else:
        my_metro = ''

    if my_metro != '':
        metro = process.extractOne(my_metro, metros,score_cutoff=80)
    else:
        metro = None
    if metro is None:
        bot_message = "Please enter a proper metro station name"
    else:
        #metro = metro(0)

        bot_message = monument_list(str(metro[0]))
        bot_message= str(bot_message)

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=bot_message))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": bot_message
        }
    })
    print(type(data))
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)




def monument_list(metro_station):
    metro_station=metro_station.lower()
    import hypertrack
    hypertrack.secret_key = 'sk_test_b002b3b4a0349e6d060bcb41f5356bef5d2a49c3'
    places = hypertrack.Place.list()

    monuments =[]
    for place in places:
        if place['landmark'] == metro_station:
            if place['name'] != metro_station:
                monuments.append(place['name'])

    monuments = [str(x.title()) for x in monuments]

    return  "\n".join(monuments)



def send_metros_list(recipient_id):
    message_text = " ".join(['Netaji Subhash Place Metro Station', 'Rajiv Chowk Metro Station ', 'Central Secretariat Metro Station', 'Chandni Chowk Metro Station', 'Qutab Minar Metro Station', 'Jor Bagh Minar Metro Station', 'Patel Chowk Metro Station', 'Hauz Khas Metro Station', 'Akshardham Temple Metro Station', 'Pragati Maidan Metro Station', 'Rajouri Garden Metro Station', 'Karol Bagh Metro Station', 'Jangpura Metro Station', 'Nehru Place Metro Station', 'Tughlaqabad Metro Station'])
    message_text = remove_non_ascii(message_text)
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    print(type(data))
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    print(type(data))
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
            print(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()
