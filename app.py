import os

from flask import Flask
from flask import request
from flask import url_for
from flask import render_template

from twilio import twiml


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


# Configure this number to a toll-free Twilio number to accept incoming calls.
@app.route('/caller', methods=['GET', 'POST'])
def caller():
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
    return str(response)


# Connect to support queue - assign to Twilio number for agent to call.
@app.route('/agent', methods=['GET', 'POST'])
def agent():
    response = twiml.Response()
    with response.dial() as dial:
        dial.queue("Queue Demo")
    return str(response)


# Installation success page.
@app.route('/')
def index():
    params = {
        'caller_request_url': url_for('.caller', _external=True),
        'agent_request_url': url_for('.agent', _external=True)}
    return render_template('index.html', params=params)


# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
