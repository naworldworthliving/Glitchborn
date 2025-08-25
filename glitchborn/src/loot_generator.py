import random
from item import Item, ItemQuality, Equipment, Consumable

# --- Item Base Data ---
EQUIPMENT_NAMES = {
    'weapon': ["Sword", "Axe", "Mace", "Dagger"],
    'head': ["Helmet", "Cap", "Coif"],
    'chest': ["Chainmail", "Plate Armor", "Leather Tunic"],
    'legs': ["Greaves", "Pants", "Leggings"]
}
CONSUMABLE_NAMES = ["Health Potion", "Stamina Potion"]

QUALITY_PREFIXES = {
    ItemQuality.POOR: ["Broken", "Rusty", "Worn"],
    ItemQuality.NORMAL: ["Common", "Standard", "Simple"],
    ItemQuality.RARE: ["Fine", "Superior", "Engraved"],
    ItemQuality.SUPER_RARE: ["Exquisite", "Masterwork", "Ornate"],
    ItemQuality.UNIQUE: ["Unbelievable", "God-Tier", "Glitch-Forged"]
}

def generate_random_item(difficulty_modifier=1.0):
    """
    Generates a random item. Higher difficulty increases the chance of better quality.
    """
    # 1. Determine Quality
    quality_roll = random.random() + (difficulty_modifier - 1.0) * 0.1

    if quality_roll > 0.98:
        quality = ItemQuality.UNIQUE
    elif quality_roll > 0.90:
        quality = ItemQuality.SUPER_RARE
    elif quality_roll > 0.75:
        quality = ItemQuality.RARE
    elif quality_roll > 0.40:
        quality = ItemQuality.NORMAL
    else:
        quality = ItemQuality.POOR

    # 2. Determine Item Type (Equipment or Consumable)
    if random.random() > 0.3: # 70% chance for equipment
        return _generate_equipment(quality)
    else: # 30% chance for consumable
        return _generate_consumable(quality)

def _generate_equipment(quality):
    """Helper function to generate a piece of equipment."""
    slot = random.choice(list(EQUIPMENT_NAMES.keys()))
    base_name = random.choice(EQUIPMENT_NAMES[slot])
    prefix = random.choice(QUALITY_PREFIXES[quality])

    name = f"{prefix} {base_name}"
    description = f"A {quality.name.lower()} {slot}."

    # Generate stats based on quality
    stat_bonus = {}
    quality_multiplier = list(ItemQuality).index(quality) + 1 # POOR=1, NORMAL=2, etc.

    if slot == 'weapon':
        stat_bonus['damage'] = random.randint(1, 3) * quality_multiplier
    else: # Armor
        stat_bonus['max_health'] = random.randint(2, 5) * quality_multiplier

    return Equipment(name, description, quality, slot, stats_bonus=stat_bonus)

def _generate_consumable(quality):
    """Helper function to generate a consumable item."""
    base_name = random.choice(CONSUMABLE_NAMES)
    prefix = random.choice(QUALITY_PREFIXES[quality])

    name = f"{prefix} {base_name}"
    description = f"A {quality.name.lower()} consumable."

    # Generate effect based on quality
    effect = {}
    quality_multiplier = list(ItemQuality).index(quality) + 1

    if "Health" in base_name:
        effect['type'] = 'heal'
        effect['amount'] = random.randint(10, 20) * quality_multiplier
    elif "Stamina" in base_name:
        effect['type'] = 'stamina_restore'
        effect['amount'] = random.randint(10, 20) * quality_multiplier

    return Consumable(name, description, quality, effect=effect)
