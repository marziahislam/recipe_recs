# recipe_recs/forms.py

from django import forms
from .models import SkillLevel, NutritionLevel

class RecipeRecommendationForm(forms.Form):
    ingredients = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter ingredients separated by commas'}),
        label='Ingredients in Fridge',
        help_text='Type the ingredients you have, separated by commas.',
        required=False  # Make field optional
    )

    skill_level = forms.ModelChoiceField(
        queryset=SkillLevel.objects.all(),  # You could also hard-code options
        label='Skill Level',
        help_text='Select your cooking skill level.',
        required=False  # Make field optional
    )

    nutrition_level = forms.ModelChoiceField(
        queryset=NutritionLevel.objects.all(),  # You could also hard-code options
        label='Nutrition Preferences',
        help_text='Select your nutrition preferences.',
        required=False  # Make field optional
    )

    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients')
        skill_level = cleaned_data.get('skill_level')
        nutrition_level = cleaned_data.get('nutrition_level')

        # Check if all fields are empty
        if not ingredients and not skill_level and not nutrition_level:
            raise forms.ValidationError("You must fill out at least one field.")
        
        return cleaned_data
