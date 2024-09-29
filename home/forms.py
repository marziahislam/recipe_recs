from django import forms
from .models import Ingredient, SkillLevel, NutritionLevel

class RecipeRecommendationForm(forms.Form):
    ingredients = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter ingredients separated by commas'}),
        label='Ingredients in Fridge',
        help_text='Type the ingredients you have, separated by commas.'
    )

    skill_level = forms.ModelChoiceField(
        queryset=SkillLevel.objects.all(),  # You could also hard-code options
        label='Skill Level',
        help_text='Select your cooking skill level.'
    )

    nutrition_level = forms.ModelChoiceField(
        queryset=NutritionLevel.objects.all(),  # You could also hard-code options
        label='Nutrition Preferences',
        help_text='Select your nutrition preferences.'
    )