from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .forms import CreateUserForm, CustomerForm, WorkoutForm, ProgressForm, MealPlanForm
from django.http import HttpResponse
from .decorators import unathenticated_user, allowed_users, admin_only
# Create your views here.

def base(request):
    return render(request, 'app/base.html')

@login_required(login_url='login')
def ahome(request):
    return render(request, 'app/home.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'app/u_home.html')

def users_list(request):
    customers = Customer.objects.all()
    return render(request, 'app/users_list.html', {'customers': customers})

@login_required(login_url='login')
@admin_only
def a_workouts(request):
    # Fetch all workouts from the database to display to the user
    workouts = Workout.objects.all()
    return render(request, 'app/a_workouts.html', {'workouts': workouts})

def workouts_view(request):
    # Assuming you have a Workout model and querying all workouts.
    workouts = Workout.objects.all()
    return render(request, 'app/u_workouts.html', {'workouts': workouts})

@login_required(login_url='login')
@admin_only
def workout_view(request):
    # Fetch all workouts from the database
    workouts = Workout.objects.all()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout_name = form.cleaned_data['name']
            workout_description = form.cleaned_data['description']
            # Save the new workout to the database
            Workout.objects.create(name=workout_name, description=workout_description)
            return redirect('workout_view')  # Redirect to the same page after POST
    else:
        form = WorkoutForm()

    return render(request, 'app/workouts.html', {'form': form, 'workouts': workouts})

@login_required(login_url='login')
@admin_only
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    
    if request.method == "POST":
        form = WorkoutForm(request.POST, request.FILES, instance=workout)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('workout_view')  # Redirect to workouts list after saving
    
    else:
        form = WorkoutForm(instance=workout)

    return render(request, 'app/edit_workout.html', {'form': form, 'workout': workout})

@login_required(login_url='login')
@admin_only
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    return redirect('workout_view')  # Redirect to the workout listing page after deletion

def myworkouts_view(request):
    myworkouts = MyWorkout.objects.all()
    return render(request, 'app/myworkouts.html', {'myworkouts': myworkouts})

def save_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    MyWorkout.objects.create(workout=workout)
    return redirect('myworkouts')

def remove_workout(request, workout_id):
    myworkout = get_object_or_404(MyWorkout, id=workout_id)
    myworkout.delete()
    return redirect('myworkouts')

@login_required
def add_progress(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            # Associate the form with the logged-in user's customer instance
            progress = form.save(commit=False)
            customer = request.user.customer  # Assuming the Customer model is linked to the User model
            progress.customer = customer  # Set the customer field to the logged-in user's customer
            progress.save()  # Save the progress instance
            return redirect('progress_list')  # Redirect to the same page after saving
    else:
        form = ProgressForm()

    # Get progress for the current user
    customer = request.user.customer  # Get the customer for the logged-in user
    progress_list = Progress.objects.filter(customer=customer)

    workouts = Workout.objects.all()
    return render(request, 'app/add_progress.html', {'form': form, 'workouts': workouts, 'progress_list': progress_list})

def progress_edit(request, pk):
    progress = get_object_or_404(Progress, pk=pk)
    
    if request.method == "POST":
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('progress_list')
    else:
        form = ProgressForm(instance=progress)
    
    return render(request, 'app/progress_form.html', {'form': form})

def progress_delete(request, pk):
    progress = get_object_or_404(Progress, pk=pk)
    
    if request.method == "POST":
        progress.delete()
        return redirect('progress_list')
    
    return render(request, 'app/progress_confirm_delete.html', {'progress': progress})

@login_required
def meal_plan_list(request):
    meal_plans = MealPlan.objects.filter(customer=request.user.customer)
    
    # Compute totals
    total_calories = sum(meal.calories for meal in meal_plans)
    total_protein = sum(meal.protein for meal in meal_plans)
    total_carbs = sum(meal.carbs for meal in meal_plans)
    total_fats = sum(meal.fats for meal in meal_plans)

    return render(request, 'app/meal_plan_list.html', {
        'meal_plans': meal_plans,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
    })

@login_required
def meal_plan_create(request):
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.customer = request.user.customer  # Assuming a one-to-one relationship
            meal_plan.save()
            return redirect('meal_plan_list')
    else:
        form = MealPlanForm()
    return render(request, 'app/meal_plan_form.html', {'form': form})

@login_required
def meal_plan_delete(request, pk):
    meal_plan = MealPlan.objects.get(id=pk, customer__user=request.user)
    if request.method == "POST":
        meal_plan.delete()
        return redirect('meal_plan_list')
    return render(request, 'app/meal_plan_confirm_delete.html', {'meal_plan': meal_plan})

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def accSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'app/acc.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Deletes the user account
        logout(request)  # Logs out the user after deletion
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to home or any other page after deletion
    
    return render(request, 'app/acc_delete.html')


@unathenticated_user
def registerPage(request):
    
    form = CreateUserForm() 
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account Registered for ' + username)

            return redirect('login')

    context = {'form':form}
    return render(request, 'app/register.html', context)
    
@unathenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Check if user is admin or regular user
            if user.is_staff:  # If user is an admin
                return redirect('ahome')  # Redirect to admin homepage
            else:  # If user is a regular user
                return redirect('home')  # Redirect to regular user's homepage
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'app/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
