from django.urls import path, include
from .views import (ChatView,
                    )


urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
]