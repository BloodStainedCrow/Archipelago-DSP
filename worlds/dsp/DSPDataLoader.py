import json
import pkgutil
from pathlib import Path

def load_tech_data():
    file = pkgutil.get_data(__name__, "data/APTechProtos.json")
    return json.loads(file)

def load_recipe_data():
    file = pkgutil.get_data(__name__, "data/RecipeProtos.json")
    return json.loads(file)
    