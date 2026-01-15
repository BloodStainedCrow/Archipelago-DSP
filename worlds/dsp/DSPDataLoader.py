import json
import pkgutil
from pathlib import Path

# Path to your JSON file
TECH_JSON_PATH = Path(__file__).parent / "data" / "APTechProtos.json"

def load_tech_data():
    file = pkgutil.get_data(__name__, "data/APTechProtos.json")
    return json.loads(file)

def load_recipe_data():
    file = pkgutil.get_data(__name__, "data/RecipeProtos.json")
    return json.loads(file)
    