from worlds.AutoWorld import WebWorld, World
from BaseClasses import Location, Item, Tutorial, MultiWorld
from . import Items, Locations, Regions, Rules

class DSPItem(Item):
    game: str = "Dyson Sphere Program"

class DSPLocation(Location):
    game: str = "Dyson Sphere Program"
    
class DSPWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Dyson Sphere Program randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Prototy"]
    )]
    theme = "dirt"

class DSPWorld(World):
    """
    Dyson Sphere Program is a sci-fi strategy game where you build and manage a factory in space.
    """
    game = 'Dyson Sphere Program'
    web = DSPWeb()
    
    item_name_to_id = {item.name: item.id for item in Items.items}
    item_name_to_item = {item.name: item for item in Items.items}
    location_name_to_id = {loc.name: loc.id for loc in Locations.locations}
    
    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        
    def create_regions(self):
        Regions.create_regions(self)
        
        # Add locations into regions
        for region in self.multiworld.get_regions(self.player):
            for loc in [location for location in Locations.locations if location.region == region.name]:
                location = DSPLocation(player=self.player, name=loc.name, address=loc.id, parent=region)
                region.locations.append(location)
    
    def create_item(self, name: str) -> DSPItem:
        item: Items.ItemDef = self.item_name_to_item[name]
        return DSPItem(name, item.classification, item.id, self.player)
    
    def set_rules(self):
        Rules.set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Mission Completed!', self.player)
    
    def create_items(self) -> None:
        for item in Items.items:
            prefill_loc = None
            if item.prefill_location:
                prefill_loc = self.get_location(item.prefill_location)
                prefill_loc.place_locked_item(DSPItem(item.name, item.classification, item.id, self.player))
            else:
                for _ in range(item.count):
                    self.multiworld.itempool.append(DSPItem(item.name, item.classification, item.id, self.player))
    