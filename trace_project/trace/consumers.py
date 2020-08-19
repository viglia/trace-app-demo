import json
from channels.generic.websocket import WebsocketConsumer
from trace.models import Trace
from trace.class_utils import TraceUtility


class TraceConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = []
        self.trace_id = None
        self.trace_utility = TraceUtility()

    def connect(self):
        if "trace_id" in self.scope['url_route']['kwargs']:
            self.trace_id = self.scope['url_route']['kwargs']['trace_id']
            self.accept()
        else:
            self.close(code=400)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        message = json.loads(text_data)
        self.trace_utility.process_message(message)
        self.messages.append(message)

        if self.trace_utility.end is not None:
            try:
                self.trace_utility.transform_data()
                trace_dump = json.dumps(
                    self.trace_utility,
                    default=lambda o: self.dict_attributes(o))
                Trace.objects.create(
                    id=self.trace_id, trace=trace_dump)
                self.send(text_data=json.dumps({
                    'message': "Trace stored. Closing the connection"
                }))
                self.close(code=1000)
            except Exception as e:
                # if the transform_data fails the integrity check
                self.send(text_data=json.dumps({
                    'message': f"Error: {str(e)}"
                }))
                self.close(code=4000)

    def dict_attributes(self, o):
        return {k: v for k, v in o.__dict__.items()
                if not k.startswith("_") and v != []}
