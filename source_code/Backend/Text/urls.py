from django.urls import path
import Text.views as views
urlpatterns = [
    path('create/', views.CreateText.as_view()),
    path('delete/', views.DeleteText.as_view()),
    path('gettexts/', views.GetTexts.as_view()),
    path('gettext/', views.GetText.as_view()),
    path('save/', views.SaveText.as_view()),
    path('gethistory/', views.GetHistory.as_view()),
    path('change_role/', views.ChangeRole.as_view()),

]