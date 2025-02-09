# Generated by Django 5.1.5 on 2025-01-30 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appGillo', '0019_remove_meal_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mealplan',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='carbs',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='fats',
        ),
        migrations.RemoveField(
            model_name='mealplan',
            name='protein',
        ),
        migrations.AddField(
            model_name='meal',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the meal', null=True),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='meals',
            field=models.ManyToManyField(help_text='Meals included in this plan', related_name='meal_plans', to='appGillo.meal'),
        ),
    ]
