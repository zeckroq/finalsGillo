from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in centimeters")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kilograms")
    fitness_goal = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='workout_images/', blank=True, null=True)  # Add this field

    def __str__(self):
        return self.name

class MyWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.workout.name
    
class Progress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    day = models.DateField()
    current_weight = models.DecimalField(max_digits=5, decimal_places=2)
    aim_weight = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True, help_text="Add any notes or thoughts about today's progress")

    def __str__(self):
        return f"Progress for {self.customer.name} on {self.day}"
        
    
class MealPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Name of the meal plan")
    calories = models.IntegerField(help_text="Total calories per day")
    protein = models.DecimalField(max_digits=5, decimal_places=2, help_text="Protein in grams")
    carbs = models.DecimalField(max_digits=5, decimal_places=2, help_text="Carbohydrates in grams")  # <-- Add default here
    fats = models.DecimalField(max_digits=5, decimal_places=2, help_text="Fats in grams")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.customer.name}"
