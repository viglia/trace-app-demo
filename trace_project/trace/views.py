from rest_framework import generics
from trace.serializers import TraceSerializer
from trace.models import Trace


class TraceList(generics.RetrieveDestroyAPIView):
    serializer_class = TraceSerializer
    queryset = Trace.objects.all()
