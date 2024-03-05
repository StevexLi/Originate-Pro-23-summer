from django.urls import path
import User.views as views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('login/', views.Login.as_view()),
    path('send_vcode/', views.SendVcode.as_view()),
    path('find_password/', views.FindPassword.as_view()),
    path('change_profile/', views.ChangeProfile.as_view()),
    path('get_profile/', views.GetUserInfo.as_view()),
    path('get_team/', views.GetAllTeam.as_view()),
    path('check_in_team/', views.CheckInTeam.as_view()),
    path('get_group/', views.GetAllGroup.as_view()),
]