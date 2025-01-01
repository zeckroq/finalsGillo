from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .forms import CreateUserForm, CustomerForm
from .decorators import unathenticated_user, allowed_users, admin_only
# Create your views here.

def base(request):
    return render(request, 'app/base.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def home(request):
    return render(request, 'app/home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def products(request):
    return render(request, 'app/products.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['users'])
def userPage(request):
    context = {}
    return render(request, 'app/user.html', context)

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

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'app/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


class FeedbackListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/workouts.html'

class FeedbackDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/feedback_detail.html'
    
class FeedbackCreateView(CreateView):   
    model = Post
    fields = ['title', 'author', 'body']
    template_name = 'app/feedback_create.html'

class FeedbackUpdateView(UpdateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name = 'app/feedback_update.html'

class FeedbackDeleteView(DeleteView):
    model = Post
    template_name = 'app/feedback_delete.html'
    success_url = reverse_lazy('feedback')