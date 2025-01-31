from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.base, name="base"),
    path('ahome/', views.ahome, name="ahome"),
    path('home/', views.home, name="home"),
    path('users/', views.users_list, name='users_list'),

    path('acc/', views.accSettings, name="acc"),
    path('delete_account/', views.delete_account, name='delete_account'),

    path('aworkout/', views.a_workouts, name="a_workout"),
    path('workout/', views.workout_view, name="workout_view"),
    path('workouts/', views.workouts_view, name='workouts_view'),

    path('edit/<int:workout_id>/', views.edit_workout, name='edit_workout'),
    path('delete/<int:workout_id>/', views.delete_workout, name='delete_workout'),
    path('save_workout/<int:workout_id>/', views.save_workout, name='save_workout'),
    path('remove_workout/<int:workout_id>/', views.remove_workout, name='remove_workout'),

    path('myworkouts/', views.myworkouts_view, name='myworkouts'),
    path('add-progress/', views.add_progress, name='progress_list'),
    path('progress/<int:pk>/edit/', views.progress_edit, name='progress_edit'),
    path('progress/<int:pk>/delete/', views.progress_delete, name='progress_delete'),

    path('meal-plans/', views.meal_plan_list, name='meal_plan_list'),
    path('meal-plans/new/', views.meal_plan_create, name='meal_plan_create'),
    path('meal-plans/delete/<int:pk>/', views.meal_plan_delete, name='meal_plan_delete'),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

  
]

