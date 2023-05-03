import threading

from django.core.mail import EmailMultiAlternatives

from rpfood import settings


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list, context=None, header=None):
        self.subject = subject
        self.content = content
        self.recipient_list = recipient_list
        self.context = context

        threading.Thread.__init__(self)

    def run(self) -> None:
        pass
        # # mail_body = render_to_string(self.template, self.context)
        # msg = EmailMultiAlternatives(self.subject, self.context, settings.EMAIL_HOST_USER, self.recipient_list)
        # # msg.attach_alternative(self.context, "text/html")
        # msg.send()


def send_email_thread(subject, content, recipient_list, context=None, header=None):
    EmailThread(subject, content, recipient_list, context, header).start()
