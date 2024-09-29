# recipe_recs/views.py
# recipe_recs/views.py
from recipe_recs import settings
from django.shortcuts import render
from .forms import RecipeRecommendationForm
from .models import Recipe
import requests

def recommend_recipe(request):
    form = RecipeRecommendationForm()
    recommended_recipes = []

    if request.method == 'POST':
        form = RecipeRecommendationForm(request.POST)
        if form.is_valid():
            skill_level = form.cleaned_data['skill_level']
            nutrition_level = form.cleaned_data['nutrition_level']
            ingredients = [ingredient.strip() for ingredient in form.cleaned_data['ingredients'].split(',')]

            # Query for recipes based on user input
            recommended_recipes = get_recipes(ingredients, skill_level, nutrition_level)

    return render(request, 'home/index.html', {'form': form, 'recipes': recommended_recipes})


def get_recipes(ingredients, skill_level=None, nutrition_level=None):
    ingredient_string = ','.join(ingredients)
    
    api_key = settings.SPOON_API_KEY
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'

    # Set up query parameters for Spoonacular API
    params = {
        'apiKey': api_key,  # Spoonacular requires apiKey for authentication
        'includeIngredients': ingredient_string,  # Comma-separated list of ingredients
        'number': 10,  # Fetch up to 10 recipes
        'addRecipeInformation': True,  # Include full recipe details in the response
    }

    # Add diet filter based on nutrition level
    if nutrition_level:
        params['diet'] = nutrition_level  # E.g., 'vegetarian', 'gluten free', etc.

    # Add skill level filtering by limiting max preparation time or number of ingredients
    if skill_level == 'Beginner':
        params['maxIngredients'] = 5  # Beginner recipes should have fewer ingredients
        params['maxReadyTime'] = 30  # Max preparation time for beginners
    elif skill_level == 'Intermediate':
        params['maxIngredients'] = 10  # Intermediate recipes have more ingredients
        params['maxReadyTime'] = 60  # Intermediate skill level allows for more cooking time

    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])  # Spoonacular returns recipes under the 'results' key
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []  # Return an empty list if there's an issue with the API call
