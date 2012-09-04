import unittest
from mock import patch

from .context import app


app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'                                     
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'                                     
app.config['TWILIO_CALLER_ID'] = '+15558675309'
app.config['AGENT_NUMBER'] = '+15556667777'


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, path='/sms', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309'):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to, 
            'From': from_,
            'Body': body,
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        return self.app.post(path, data=params)

    def call(self, url='/voice', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', digits=None, extra_params=None):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'CallStatus': 'ringing',
            'Direction': 'inbound',
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if digits:
            params['Digits'] = digits
        if extra_params:
            params = dict(params.items() + extra_params.items())
        return self.app.post(url, data=params)


class TwilioTests(TwiMLTest):
    def test_caller(self):
        response = self.call(url='/caller')
        self.assertTwiML(response)

    def test_agent(self):
        response = self.call(url='/agent')
        self.assertTwiML(response)

    @patch('twilio.rest.resources.SmsMessages', autospec=True)    
    def test_wait(self, MockMessages):
        app.twilio_client.sms.messages = MockMessages.return_value
        app.twilio_client.sms.messages.create.return_value = True

        response = self.call(url='/wait', extra_params={'QueuePosition': '1'})

        self.assertTwiML(response)
        app.twilio_client.sms.messages.create.assert_called_with(
            from_=app.config['TWILIO_CALLER_ID'],
            to=app.config['AGENT_NUMBER'],
            body="A caller is waiting in the support queue. " \
                    "Call this number to answer.")
