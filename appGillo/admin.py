from django.contrib import admin

# Register your models here.

from .models import Customer
from .models import Workout
from .models import MyWorkout
from .models import Progress
from .models import MealPlan

admin.site.register(Customer)
admin.site.register(Workout)
admin.site.register(MyWorkout)
admin.site.register(Progress)
admin.site.register(MealPlan)