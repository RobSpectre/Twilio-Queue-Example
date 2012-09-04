# Twilio Queue Example

A hackpack example using Twilio's new
[Queue](http://www.twilio.com/docs/api/twiml/queue) verb to create a call-in
queue.  Not into Python?  Check out examples in other languages in the
[Twilio Howto](http://www.twilio.com/docs/howto/callqueue).

[![Build
Status](https://secure.travis-ci.org/RobSpectre/Twilio-Queue-Example.png)]
(http://travis-ci.org/RobSpectre/Twilio-Queue-Example)


## Features

Holy biscuits! It's got features!

* _Caller Handling_ - Take callers and put
  them in a call queue with TwiML's new
  [Enqueue](http://www.twilio.com/docs/api/twiml/enqueue) verb.  
* _Agent Handling_ - Answers callers in the order they dialed in using TwiML's
  new [Queue](http://www.twilio.com/docs/api/twiml/queue) noun.
* Automagic Configuration - Just run `python configure.py --account_sid ACxxxx --auth_token yyyyy` 
  and this hackpack will Twilio and Heroku for you.
* Plug-and-Play - Procfile, requirements.txt and Makefile make installation
  and usage a breeze.
* Testing - Totally tested with examples for you to use in your larger
  implementations. 
* [PEP8](http://www.python.org/dev/peps/pep-0008/) - It's good for you!

## Usage

Install using the Getting Started instructions below and configure a pair of
Twilio Phone Numbers with the two links provided - one for callers and one for
agents.

![Success
page](https://raw.github.com/RobSpectre/Twilio-Queue-Example/master/static/images/screenshot.png)

Callers are the people who are placed into the Queue, while Agents are the
people who answer them.  In most implementations, "callers" can be considered
customers who need support and "agents" are the service representatives
responsible for providing it.

To use this app, purchase two Twilio Phone Numbers and configure one number to
use the Caller Voice Request URL and the other to use the Agent Voice Request
URL.

For an example in action, be sure to check out [Jon Gottfried's
screencast](https://www.youtube.com/watch?v=AICLFi2djbs).

## Installation

Step-by-step on how to deploy, configure and develop on this hackpack.

### Getting Started 

0) Get the requirements:

* [git](http://git-scm.com/)
* [Heroku Toolbelt](https://toolbelt.heroku.com/)
* [Python](http://python.org/download/)

1) Grab latest source
<pre>
git clone git://github.com/RobSpectre/Twilio-Queue-Example.git 
</pre>

2) Navigate to folder and create new Heroku Cedar app
<pre>
heroku create
</pre>

3) Deploy to Heroku
<pre>
git push heroku master
</pre>

4) Scale your dynos
<pre>
heroku scale web=1
</pre>

5) Visit the home page of your new Heroku app to see your newly configured app!
<pre>
heroku open
</pre>


### Configuration

Configure your hackpack with three easy options.

#### Automagic Configuration

This hackpack ships with an auto-configure script that will create a new TwiML
app, purchase a new phone number, and set your Heroku app's environment
variables to use your new settings.  Here's a quick step-by-step:

1) Make sure you have all dependencies installed
<pre>
make init
</pre>

2) Run configure script and follow instructions.
<pre>
python configure.py --account_sid ACxxxxxx --auth_token yyyyyyy
</pre>

3) For local development, copy/paste the environment variable commands the
configurator provides to your shell.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
</pre>

Automagic configuration comes with a number of features.  
`python configure.py --help` to see them all.


#### local_settings.py

local_settings.py is a file available in the hackpack route for you to configure
your twilio account credentials manually.  Be sure not to expose your Twilio
account to a public repo though.

```python
ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
```

#### Setting Your Own Environment Variables

The configurator will automatically use your environment variables if you
already have a TwiML app and phone number you would prefer to use.  When these
environment variables are present, it will configure the Twilio and Heroku apps
all to use the hackpack.

1) Set environment variables locally.
<pre>
export TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxx
export TWILIO_AUTH_TOKEN=yyyyyyyyyyyyyyyyy
export TWILIO_APP_SID=APzzzzzzzzzzzzzzzzzz
export TWILIO_CALLER_ID=+15556667777
</pre>

2) Run configurator
<pre>
python configure.py
</pre>


### Development

Getting your local environment setup to work with this hackpack is similarly
easy.  After you configure your hackpack with the steps above, use this guide to
get going locally:

1) Install the dependencies.
<pre>
make init
</pre>

2) Launch local development webserver
<pre>
foreman start
</pre>

3) Open browser to [http://localhost:5000](http://localhost:5000).

4) Tweak away on `app.py`.


## Testing

This hackpack comes with a full testing suite ready for nose.

<pre>
make test
</pre>


## Meta 

* No warranty expressed or implied.  Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by [Twilio New
 York](http://www.meetup.com/Twilio/New-York-NY/) 
