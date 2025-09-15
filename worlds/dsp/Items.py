from BaseClasses import ItemClassification
from typing import List, Optional
from .DSPItemTypeEnum import DSPType
from .DSPDataLoader import load_tech_data, ensure_unique_name

class ItemDef:
    def __init__(self,
                    type: Optional[DSPType],
                    id: Optional[int],
                    name: str,
                    classification: ItemClassification,
                    count: int,
                    prefill_location: Optional[str] = None):
        self.type = type
        self.id = id
        self.name = name
        self.classification = classification
        self.count = count
        self.prefill_location = prefill_location

# Progression recipe IDs
PROGRESSION_RECIPE_IDS = {9, 10, 18, 27, 55, 75, 102}

# Load tech data
tech_data = load_tech_data()

# Build items
items: List[ItemDef] = []

used_item_names = {}

for tech in tech_data:
    if tech.get("IsHiddenTech"):
        continue  # Skip hidden tech

    tech_id = tech.get("ID")
    if tech_id == 1:
        continue # Skip the initial tech
    
    tech_name = tech.get("Name")
    unlock_recipes = set(tech.get("UnlockRecipes", []))

    classification = (
        ItemClassification.progression
        if unlock_recipes.intersection(PROGRESSION_RECIPE_IDS)
        else ItemClassification.filler
    )

    # Get unique name
    unique_name = ensure_unique_name(tech_name, used_item_names)
    
    item = ItemDef(
        type=DSPType.ITEM,
        id=tech_id,
        name=unique_name,
        classification=classification,
        count=1,
        prefill_location=None,
    )

    items.append(item)

# Add completion item
items.append(ItemDef(None, None, 'Mission Completed!', ItemClassification.progression, 1, 'Mission Completed!'))