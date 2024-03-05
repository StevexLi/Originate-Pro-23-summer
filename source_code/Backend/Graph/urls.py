from django.urls import path
import Graph.views as views
urlpatterns = [
    path('create/', views.CreateGraph.as_view()),
    path('delete/', views.DeleteGraph.as_view()),
    path('getgraphs/', views.GetGraphs.as_view()),
    path('getgraph/', views.GetGraph.as_view()),
    path('save/', views.SaveGraph.as_view()),
]