from rest_framework import generics
from TraceApp.serializers import TraceSerializer
from .models import Trace


class TraceList(generics.RetrieveDestroyAPIView):
    serializer_class = TraceSerializer
    queryset = Trace.objects.all()
