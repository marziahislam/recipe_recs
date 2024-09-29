

from django import forms


SKILL_LEVEL_CHOICES = [
    ('', 'None'),
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

NUTRITION_LEVEL_CHOICES = [
    ('', 'None'),
    ('Gluten Free', 'Gluten Free'),
    ('Ketogenic', 'Ketogenic'),
    ('Vegetarian', 'Vegetarian'),
    ('Vegan', 'Vegan'),
    ('Paleo', 'Paleo'),
    ('Pescetarian', 'Pescetarian'),
    ('Low-calorie', 'Low-calorie'),
    ('Low-carb', 'Low-carb'),
    ('High-protein', 'High-protein'),
]

class RecipeRecommendationForm(forms.Form):
    ingredients = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter ingredients separated by commas'}),
        label='Ingredients Available',
        help_text='Enter ingredients: ',
        required=False  
    )

    skill_level = forms.ChoiceField(
        choices=SKILL_LEVEL_CHOICES,
        label='Cooking Skill Level',
        help_text='Select your cooking skill level.',
        required=False  
    )

    nutrition_level = forms.ChoiceField(
        choices=NUTRITION_LEVEL_CHOICES,
        label='Nutrition Preferences',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients')
        skill_level = cleaned_data.get('skill_level')
        nutrition_level = cleaned_data.get('nutrition_level')

        
        if not ingredients and not skill_level and not nutrition_level:
            raise forms.ValidationError("You must fill out at least one field.")
        
        return cleaned_data
