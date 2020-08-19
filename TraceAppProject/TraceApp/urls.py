from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from TraceApp.consumers import TraceConsumer
from TraceApp import views

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),

    path("trace/<int:pk>/",
         views.TraceList.as_view(),
         name="trace-detail")
]

websocket_urlpatterns = [
    re_path(r'^ws/trace/(?P<trace_id>\d+)$', TraceConsumer),
]
