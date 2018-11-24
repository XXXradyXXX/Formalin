import sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot, Element, Button

from pprint import pprint


app = Flask(__name__)

# Facebook apps link:   https://developers.facebook.com/apps/2222049801408664/dashboard/
FB_ACCESS_TOKEN = "EAACZCFZCMSQ4QBALkTb5XvN9wFZBTfZAi1zdvTVIUlpa18AK2LbJ0ZAzWnZBsX9rBFZAsPQ8kgYWfhnfNo2M1EzKc3pK9m6QiZBVXURZCzyUSRZAAXvVzOSu7WNJnyHwHRV1dlbdZBKTIL5fLqfNazRLYDsroI6q6vCuCuNQ8dbpm5VSQZDZD"

bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World Set Token", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # **Necessary Code that extract json data facebook send**
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    # add for image reply
                    elif 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['attachments']

                    else:
                        messaging_text = 'no text'

                    response = None
                    entity, value = wit_response(messaging_text)

                    if entity == 'greetings':
                        response = " অাপনি কেমন আছেন"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'Get_Started':
                        response = " Do you want to know how to start income using Adsense"
                        bot.send_text_message(sender_id, response)


                    elif entity == 'thanks':
                        response = " ভাল থাকবেন ।"
                        bot.send_text_message(sender_id, response)

                    if response == None:
                        response = "আমি যাতে যোগ্যতা যাচাই করতে পারি ,তাই আপনার তথ্য দিন । নিচের লিংকে একটা ফর্ম আছে সেটি পুরন করুন । https://sites.google.com/view/human-migration-services/ "
                        bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(port=80, use_reloader=True)
