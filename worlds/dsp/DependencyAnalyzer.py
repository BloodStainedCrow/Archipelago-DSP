from collections import defaultdict
from typing import Dict, List, Set
from DSPDataLoader import load_tech_data, load_recipe_data

"""
This file is never called in the apworld, but useful for DSP AP devs to analyze tech dependencies.
"""

# Load data
tech_data = load_tech_data()
recipe_data = load_recipe_data()

# Constants
MATRIX_ITEM_IDS = set(range(6001, 6007))       # 6001 to 6006 inclusive
DEFAULT_RECIPE_IDS = {1, 2, 3, 4, 5, 6, 50}     # Recipes unlocked by default
NON_RECIPE_ITEM_IDS = {1006, 1030}             # Items gathered from the world (log, coal, etc.)

# Lookup tables
item_to_producing_recipes: Dict[int, List[int]] = defaultdict(list)
for recipe in recipe_data:
    for result_item in recipe.get("Results", []):
        item_to_producing_recipes[result_item].append(recipe["ID"])

recipe_to_tech: Dict[int, int] = {}
for tech in tech_data:
    for recipe_id in tech.get("UnlockRecipes", []):
        recipe_to_tech[recipe_id] = tech["ID"]

# Dependency maps
tech_dependencies: Dict[int, Set[int]] = defaultdict(set)
unknown_dependencies: Dict[int, Set[int]] = defaultdict(set)

# Dependency resolution
for tech in tech_data:
    if tech.get("IsHiddenTech"):
        continue
    current_tech_id = tech["ID"]
    if current_tech_id == 1:
        continue  # Skip initial tech

    required_items = tech.get("Items", [])

    for item_id in required_items:
        # Skip items that don't require unlocking
        if item_id in MATRIX_ITEM_IDS or item_id in NON_RECIPE_ITEM_IDS:
            continue

        producing_recipes = item_to_producing_recipes.get(item_id, [])
        if not producing_recipes:
            unknown_dependencies[current_tech_id].add(item_id)
            continue

        found_dependency = False
        for recipe_id in producing_recipes:
            if recipe_id in DEFAULT_RECIPE_IDS:
                found_dependency = True
                continue

            unlocking_tech_id = recipe_to_tech.get(recipe_id)
            if unlocking_tech_id and unlocking_tech_id != current_tech_id:
                tech_dependencies[current_tech_id].add(unlocking_tech_id)
                found_dependency = True

        if not found_dependency:
            unknown_dependencies[current_tech_id].add(item_id)

# Output
print("=== Tech Dependencies ===")
for tech_id, deps in tech_dependencies.items():
    if deps:
        print(f"Tech {tech_id} depends on: {sorted(deps)}")

print("\n=== Unknown Dependencies (manual review needed) ===")
for tech_id, items in unknown_dependencies.items():
    print(f"Tech {tech_id} has unknown dependencies on items: {sorted(items)}")
