from django.urls import path
from .views import *
urlpatterns = [
    path('create/', CreateTeam.as_view()),
    path('break_up/', BreakUpTeam.as_view()),
    path('change_auth/', ChangeAuth.as_view()),
    path('invite/', InviteMember.as_view()),
    path('get_info/', GetInfo.as_view()),
    path('change_profile/', ChangeTeamProfile.as_view()),
]
