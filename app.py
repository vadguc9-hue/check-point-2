import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "recipe_secret_key_2026"  # Required for flash messages
DATA_FILE = 'recipes.json'

# --- HELPER FUNCTIONS (Persistence & Error Handling) ---
def load_recipes():
    """Reads recipes from JSON. Handles file-not-found and empty files."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Error handling: If file is corrupted, return empty list
        return []

def save_recipes(recipes):
    """Writes the list back to JSON."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(recipes, f, indent=4)
    except IOError:
        flash("Critical Error: Could not write to database!", "danger")

# --- ROUTES (The 5 Required Routes) ---

@app.route('/')
def home():
    """READ (All): The Home page."""
    recipes = load_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<string:recipe_id>')
def view_recipe(recipe_id):
    """READ (One): The Detail page."""
    recipes = load_recipes()
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if not recipe:
        flash("Recipe not found!", "warning")
        return redirect(url_for('home'))
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/create', methods=['GET', 'POST'])
def create():
    """CREATE: Add a new recipe."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        
        # Server-side Validation
        if not name or not ingredients:
            flash("Name and Ingredients are required!", "danger")
            return redirect(url_for('create'))

        recipes = load_recipes()
        new_recipe = {
            "id": str(uuid4()), # Generates unique ID
            "name": name,
            "category": request.form.get('category'),
            "rating": request.form.get('rating', 5),
            "ingredients": ingredients,
            "instructions": request.form.get('instructions', '')
        }
        recipes.append(new_recipe)
        save_recipes(recipes)
        flash(f"Success! '{name}' has been added.", "success")
        return redirect(url_for('home'))
    
    return render_template('add_recipe.html')

@app.route('/edit/<string:recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
    """UPDATE: Modify an existing recipe."""
    recipes = load_recipes()
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)

    if not recipe:
        flash("Error: Recipe not found.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        recipe['name'] = request.form.get('name')
        recipe['category'] = request.form.get('category')
        recipe['rating'] = request.form.get('rating')
        recipe['ingredients'] = request.form.get('ingredients')
        recipe['instructions'] = request.form.get('instructions')
        
        save_recipes(recipes)
        flash("Recipe updated successfully!", "success")
        return redirect(url_for('home'))

    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/delete/<string:recipe_id>')
def delete(recipe_id):
    """DELETE: Remove a recipe."""
    recipes = load_recipes()
    # Logic: Keep everything EXCEPT the id we want to delete
    original_count = len(recipes)
    recipes = [r for r in recipes if r['id'] != recipe_id]

    if len(recipes) < original_count:
        save_recipes(recipes)
        flash("Recipe deleted forever.", "info")
    else:
        flash("Delete failed: Recipe not found.", "danger")
        
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)