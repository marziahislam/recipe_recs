from django import forms
from .models import SkillLevel, NutritionLevel, Ingredient

class RecipeRecommendationForm(forms.Form):
    skill_level = forms.ModelChoiceField(queryset=SkillLevel.objects.all(), required=True, label="Skill Level")
    nutrition_level = forms.ModelChoiceField(queryset=NutritionLevel.objects.all(), required=True, label="Nutrition Level")
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label="Ingredients in Fridge")