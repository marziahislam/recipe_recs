

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

            
            recommended_recipes = get_recipes(ingredients, skill_level, nutrition_level)

    return render(request, 'home/index.html', {'form': form, 'recipes': recommended_recipes})

def get_recipes(ingredients, skill_level=None, nutrition_level=None):
    api_key = settings.SPOON_API_KEY
    base_url = 'https://api.spoonacular.com/recipes/complexSearch'

    ingredient_string = ','.join(ingredients)

    
    params = {
        'apiKey': api_key,
        'includeIngredients': ingredient_string,
        'number': 10,
        'addRecipeInformation': True,  
        'instructionsRequired': True,  
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

    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        recipes = data.get('results', [])

        for recipe in recipes:
            recipe['all_ingredients'] = []  
            recipe['image'] = recipe.get('image')  
            recipe['readyInMinutes'] = recipe.get('readyInMinutes')  

            for instruction in recipe.get('analyzedInstructions', []):
                for step in instruction.get('steps', []):
                    for ingredient in step.get('ingredients', []):
                        
                        if 'name' in ingredient:
                            recipe['all_ingredients'].append(ingredient['name'])
        return recipes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []  



