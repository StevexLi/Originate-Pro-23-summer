from django.urls import path
import Project.views as views
urlpatterns = [
    path('create/', views.CreateProject.as_view()),
    path('delete/', views.DeleteProject.as_view()),
    path('update/', views.UpdateProject.as_view()),
    path('restore/', views.RestoreProject.as_view()),
    path('remove/',views.RemoveProject.as_view()),
    path('empty/', views.EmptyRecycleBin.as_view()),
    path('getinfo/', views.Getinfo.as_view()),
    path('get_deletelist/', views.GetDeletelist.as_view()),
    path('copy/', views.CopyProject.as_view()),
    path('change_role/', views.ChangeRole.as_view()),
]
