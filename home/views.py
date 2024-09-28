from django.shortcuts import render
from .forms import RecipeRecommendationForm
from .models import Recipe

def recommend_recipe(request):
    if request.method == 'POST':
        form = RecipeRecommendationForm(request.POST)
        if form.is_valid():
            skill_level = form.cleaned_data['skill_level']
            nutrition_level = form.cleaned_data['nutrition_level']
            ingredients = form.cleaned_data['ingredients']

            # Query for recipes based on user input
            recommended_recipes = Recipe.objects.filter(
                skill_level=skill_level,
                nutrition_level=nutrition_level,
                ingredients__in=ingredients
            ).distinct()

            return render(request, 'home/results.html', {'recipes': recommended_recipes})

    else:
        form = RecipeRecommendationForm()

    return render(request, 'home/index.html', {'form': form})