""" handles mail sending for verification and reset password"""
from twilio.rest import Client
import os
import random

class Mail():
    def __init__(self, receiver):
        self.sender = "chating.speech@gmail.com"
        self.receiver = '+972' + receiver
        self.code = self.generate_code()
        account_sid = sid
        auth_token = token
        client = Client(account_sid, auth_token)

        msg = client.messages.create(
            body=f"Hello, your code is {self.code}",
            from_='+12056192253',
            to=str(self.receiver))

        print(msg.sid)

    def generate_code(self):
        # generate 4 digit code to send user
        self.code = str(random.randint(1000, 9999))
        return self.code

    def get_code(self):
        return self.code


m = Mail("0523671576")