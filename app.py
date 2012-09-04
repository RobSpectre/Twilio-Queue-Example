import os

from flask import Flask
from flask import request

from twilio import twiml
from twilio.rest import TwilioRestClient


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')
app.twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_AUTH_TOKEN'])


# Configure this number to a toll-free Twilio number to accept incoming calls.
@app.route('/voice', methods=['GET', 'POST'])
def enqueue():
    response = twiml.Response()
    response.say("Thank you for calling this demonstration of Twilio Queue " \
            "Please hold.")
    response.enqueue("Queue Demo", waitUrl='/wait')
    return str(response)


# Configure waiting room to notify user of current position in the queue and
# play the sweet, soothing sounds of Twilio's coffeeshop collection.
@app.route('/wait', methods=['GET', 'POST'])
def wait():
    response = twiml.Response()
    response.say("You are number %s in line." % request.form['QueuePosition'])
    response.play("http://com.twilio.music.guitars.s3.amazonaws.com/" \
            "Pitx_-_A_Thought.mp3")
    response.play("http://com.twilio.music.guitars.s3.amazonaws.com/" \
            "Pitx_-_Long_Winter.mp3")
    response.redirect('/wait')

    # Notify agent of call via SMS
    if app.config['AGENT_NUMBER']:
        app.twilio_client.sms.messages.create(
            from_=app.config['TWILIO_CALLER_ID'],
            to=app.config['AGENT_NUMBER'],
            body="A caller is waiting in the support queue. " \
                    "Call this number to answer.")
    return str(response)


# Connect to support queue - assign to Twilio number for agent to call.
@app.route('/queue', methods=['GET', 'POST'])
def queue():
    response = twiml.Response()
    with response.dial() as dial:
        dial.queue("Queue Demo")
    return str(response)


# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
