from django.urls import path
from . import views 
from .views import (FeedbackListView, FeedbackDetailView, FeedbackCreateView, FeedbackUpdateView, FeedbackDeleteView)

urlpatterns = [
    path('', views.base, name="base"),
    path('home/', views.home, name="home"),
    path('acc/', views.accSettings, name="acc"),
    path('products/', views.products, name="products"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user"),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('feedback/', FeedbackListView.as_view(), name='feedback'),
    path('feedback/<int:pk>', FeedbackDetailView.as_view(), name='feedback_detail'),
    path('feedback/create', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/edit', FeedbackUpdateView.as_view(), name='feedback_update'),
    path('feedback/<int:pk>/delete', FeedbackDeleteView.as_view(), name='feedback_delete'),
  
]