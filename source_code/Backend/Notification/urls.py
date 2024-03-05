from django.urls import path
from .views import CreateNotification
urlpatterns = [
    path('create/', CreateNotification.as_view()),
]