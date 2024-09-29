# recipe_recs/views.py
# recipe_recs/views.py
from recipe_recs import settings
from django.shortcuts import render
from .forms import RecipeRecommendationForm
from .models import Recipe
import requests
import json

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
        'apiKey': api_key,
        'includeIngredients': ingredient_string,
        'number': 10,
        'addRecipeInformation': True,  # Make sure this is True
        'instructionsRequired': True,  # Optional: only return recipes with instructions
    }

    if nutrition_level:
        params['diet'] = nutrition_level

    if skill_level == 'Beginner':
        params['maxIngredients'] = 5
        params['maxReadyTime'] = 30
    elif skill_level == 'Intermediate':
        params['maxIngredients'] = 10
        params['maxReadyTime'] = 60
    elif skill_level == 'Advanced':
        pass

    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = data.get('results', [])

        # Process recipes to extract ingredients from analyzed instructions
        for recipe in recipes:
            recipe['all_ingredients'] = []  # Initialize list to hold all ingredients
            recipe['image'] = recipe.get('image')  # Get the recipe image
            recipe['readyInMinutes'] = recipe.get('readyInMinutes')  # Get the preparation time

            # Loop through analyzed instructions
            for instruction in recipe.get('analyzedInstructions', []):
                for step in instruction.get('steps', []):
                    for ingredient in step.get('ingredients', []):
                        # Ensure the ingredient has the necessary fields before appending
                        if 'name' in ingredient:
                            recipe['all_ingredients'].append(ingredient['name'])

        print(json.dumps(data['results'], indent=2))  # Print only the relevant part of the response
        return recipes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []  # Return an empty list if there's an issue with the API call



