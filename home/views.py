# recipe_recs/views.py

from django.shortcuts import render
import requests

from recipe_recs import settings
from .forms import RecipeRecommendationForm
from .models import Recipe  # Ensure this model is defined with fields for skill level, nutrition level, and ingredients

def recommend_recipe(request):
    if request.method == 'POST':
        form = RecipeRecommendationForm(request.POST)
        if form.is_valid():
            skill_level = form.cleaned_data['skill_level']
            nutrition_level = form.cleaned_data['nutrition_level']
            ingredients = [ingredient.strip() for ingredient in form.cleaned_data['ingredients'].split(',')]

            # Check if ingredients_input is a string and split if necessary
            if isinstance(ingredients, str):
                ingredientsNew = [ingredient.strip() for ingredient in ingredients.split(',')]
            elif isinstance(ingredients, list):
                ingredientsNew = [ingredient.strip() for ingredient in ingredients]  # If it's already a list, just strip whitespace

            # Query for recipes based on user input
            recommended_recipes = get_recipes(ingredients, skill_level, nutrition_level)

            return render(request, 'home/results.html', {'recipes': recommended_recipes})

    else:
        form = RecipeRecommendationForm()

    return render(request, 'home/index.html', {'form': form})

def get_recipes(ingredients, skill_level=None, nutrition_level=None):
    app_id = settings.EDAMAM_APP_ID
    app_key = settings.EDAMAM_APP_KEY

    ingredient_string = ','.join(ingredients)

    # Construct the URL with the ingredients
    url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(ingredient_string, app_id, app_key)

    # Set up query parameters
    params = {
        'q': ','.join(ingredients),  # Comma-separated list of ingredients
        'app_id': app_id,
        'app_key': app_key,
        'from': 0,
        'to': 10,  # Fetch the top 10 recipes
    }

    # Add diet or health filters based on nutrition level
    if nutrition_level:
        params['health'] = nutrition_level  # Corrected to 'health' for health filters like 'low-sugar', 'high-protein', etc.
    
    # Add skill level filtering
    if skill_level == 'Beginner':
        # Beginners: recipes with fewer ingredients (e.g., <= 5 ingredients)
        params['ingr'] = 5
    elif skill_level == 'Intermediate':
        # Intermediate: recipes with a moderate number of ingredients (e.g., <= 10 ingredients)
        params['ingr'] = 10
    # For advanced, we don't filter by the number of ingredients

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('hits', [])  # List of recipes
    else:
        return []  # Return empty list if there's an issue with the API call
