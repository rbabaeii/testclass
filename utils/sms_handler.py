import threading
from kavesms.kavenegar import *
from django.conf import settings


def send_sms(recipient, content):
    api = KavenegarAPI(f'{settings.SMS_API_KEY}')
    params = {
        'sender': f'{settings.SMS_SEND_FROM}',
        'receptor': recipient,
        'message': content
    }
    response = api.sms_send(params)


class SMSThread(threading.Thread):
    def __init__(self, recipient, content):
        self.content = content
        self.recipient = recipient

        threading.Thread.__init__(self)

    def run(self) -> None:
        send_sms(self.recipient, self.content)


def send_sms_thread(recipient, content):
    SMSThread(recipient, content).start()