from django.db import close_old_connections
from channels.generic.websocket import WebsocketConsumer


class BaseConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(BaseConsumer, self).__init__(*args, **kwargs)
        self.user = None

    def close_with_message(self, content):
        self.send(text_data=f'\r\n\x1b[31m{content}\x1b[0m\r\n')
        self.close()

    def connect(self):
        self.accept()
