from channels.generic.websocket import WebsocketConsumer
from .utils import BaseConsumer
import json


class SshConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        self.id = self.scope['url_route']['kwargs']['id']
        self.chan = None
        self.ssh = None

    def receive(self, text_data=None, bytes_data=None):
        data = text_data or bytes_data
        if data and self.chan:
            data = json.loads(data)
            resize = data.get('resize')
            if resize and len(resize) == 2:
                self.chan.resize_pty(*resize)
            else:
                self.chan.send(data['data'])

    def disconnect(self, code):
        if self.chan:
            self.chan.close()
        if self.ssh:
            self.ssh.close()
