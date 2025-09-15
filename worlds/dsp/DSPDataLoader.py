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
    
def ensure_unique_name(name: str, used_names: dict) -> str:
    """Ensure unique name by appending a counter if necessary."""
    if name not in used_names:
        used_names[name] = 1
        return name
    else:
        used_names[name] += 1
        return f"{name} {used_names[name]}"