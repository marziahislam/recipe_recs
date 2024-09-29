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
    api_key = settings.SPOON_API_KEY
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'

    ingredient_string = ','.join(ingredients)

    # Set up query parameters for Spoonacular API
    params = {
        'apiKey': api_key,  # API key for authentication
        'includeIngredients': ingredient_string,  # Comma-separated list of ingredients
        'number': 10,  # Fetch up to 10 recipes
        'addRecipeInformation': True,  # Include full recipe details in the response
    }

    # Add diet filter based on nutrition level
    if nutrition_level:
        params['diet'] = nutrition_level  # E.g., 'vegetarian', 'gluten free', etc.

    # Add skill level filtering
    if skill_level == 'Beginner':
        params['maxIngredients'] = 5  # Recipes for beginners with fewer ingredients
        params['maxReadyTime'] = 30  # Recipes that can be prepared in 30 minutes or less
    elif skill_level == 'Intermediate':
        params['maxIngredients'] = 10  # Recipes for intermediate cooks with up to 10 ingredients
        params['maxReadyTime'] = 60  # Recipes that take up to 60 minutes to prepare
    elif skill_level == 'Advanced':
        # For advanced users, no restrictions on ingredients or time
        # You can add more complex filters for advanced if desired
        pass

    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('results', [])  # Spoonacular returns recipes under the 'results' key
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []  # Return an empty list if there's an issue with the API call
