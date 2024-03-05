from django.urls import path
from Chat import views
urlpatterns = [
    path('history/', views.GetHistory.as_view()),
    path('invite/', views.GroupInvite.as_view()),
    path('create/', views.CreateGroupChat.as_view()),
    path('break_up/', views.BreakUpGroup.as_view()),
    path('exit/', views.ExitGroup.as_view()),
]