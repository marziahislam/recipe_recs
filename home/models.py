from django.db import models

class SkillLevel(models.Model):
    level_name = models.CharField(max_length=50)

    def __str__(self):
        return self.level_name

class NutritionLevel(models.Model):
    nutrition_type = models.CharField(max_length=100)
    max_calories = models.IntegerField()

    def __str__(self):
        return self.nutrition_type

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    skill_level = models.ForeignKey(SkillLevel, on_delete=models.CASCADE)
    nutrition_level = models.ForeignKey(NutritionLevel, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()

    def __str__(self):
        return self.name