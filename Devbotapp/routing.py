from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/code-generation/(?P<project_id>\w+)/$', consumers.CodeGenerationConsumer.as_asgi()),
]
