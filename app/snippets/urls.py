from django.urls import path
from snippets import views

urlpatterns = [
    path('create/', views.SnippetCreateView.as_view(), name='SnippetCreateView'),
    path('detail/<int:pk>/', views.SnippetDetailView.as_view(), name='SnippetDetailView'),
    path('update/<int:pk>/', views.SnippetUpdateView.as_view(), name='SnippetUpdateView'),
    path('delete/<int:pk>/', views.SnippetDeleteView.as_view(), name='SnippetDeleteView'),
    path('tags/', views.TagListView.as_view(), name='TagListView'),
    path('tags/<int:tag_id>/', views.TagDetailView.as_view(), name='TagDetailView'),
    path('', views.SnippetOverviewView.as_view(), name='SnippetOverviewView'),
]