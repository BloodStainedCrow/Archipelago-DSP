from BaseClasses import ItemClassification
from typing import List, Optional
from .DSPItemTypeEnum import DSPType
from .DSPDataLoader import load_tech_data, ensure_unique_name
import re

class ItemDef:
    def __init__(self,
                 type: Optional[DSPType],
                 id: Optional[int],
                 name: str,
                 classification: ItemClassification,
                 count: int,
                 prefill_location: Optional[str] = None,
                 progressive_group: Optional[str] = None):
        self.type = type
        self.id = id
        self.name = name
        self.classification = classification
        self.count = count
        self.prefill_location = prefill_location
        self.progressive_group = progressive_group

# Recipe IDs that are always progression
PROGRESSION_RECIPE_IDS = {9, 10, 18, 27, 55, 75, 102}

# Tech IDs that are optionally progression for balacing reasons (enabled by default)
BALANCED_PROGRESSION_TECH_IDS = {1201, 1401, 1601, 1001}

# Load tech data
tech_data = load_tech_data()

# Build items
items: List[ItemDef] = []

used_item_names = {}

# Progressive items grouped by their base name
progressive_items_by_group = {}

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
        if (unlock_recipes.intersection(PROGRESSION_RECIPE_IDS) or
            tech_id in BALANCED_PROGRESSION_TECH_IDS)
        else ItemClassification.filler
    )

    # Get unique name
    unique_name = ensure_unique_name(tech_name, used_item_names)
    
    
    progressive_group = None

    if tech_id >= 2000:
        # Extract base name (e.g., "Engine Upgrade" from "Engine Upgrade 3")
        match = re.match(r"^(.*?)(?: \d+)?$", tech_name)
        if match:
            base_name = match.group(1).strip()
            progressive_group = base_name

            # Store in dictionary for later reference if needed
            progressive_items_by_group.setdefault(base_name, []).append(tech_id)
    
    item = ItemDef(
        type=DSPType.ITEM,
        id=tech_id,
        name=unique_name,
        classification=classification,
        count=1,
        prefill_location=None,
        progressive_group=progressive_group
    )

    items.append(item)

# Add completion item
items.append(ItemDef(None, None, 'Mission Completed!', ItemClassification.progression, 1, 'Mission Completed!'))