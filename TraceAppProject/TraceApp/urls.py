from django.urls import re_path
from TraceApp.consumers import TraceConsumer

websocket_urlpatterns = [
    re_path(r'^ws/trace/(?P<trace_id>\d+)$', TraceConsumer),
]
