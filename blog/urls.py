from django.urls import path
from . import views

app_name = 'blog'  # пространство имен

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='list'),
    path('create/', views.BlogPostCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BlogPostDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='delete'),
]