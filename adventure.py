import random

def display_player_status(player_stats):
    """Displays the player's current health and attack power."""
    print(f"\nPlayer Status: Health = {player_stats['health']}, Attack = {player_stats['attack']}")

def discover_artifact(player_stats, artifacts, artifact_name):
    """Handles discovering an artifact and applying its effects to the player."""
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"You found {artifact_name}: {artifact['description']}")
        
        if artifact['effect'] == "increases health":
            player_stats['health'] += artifact['power']
            print(f"Your health increases by {artifact['power']}!")
        elif artifact['effect'] == "enhances attack":
            player_stats['attack'] += artifact['power']
            print(f"Your attack increases by {artifact['power']}!")
        
        del artifacts[artifact_name]  # Remove artifact after discovery
    else:
        print("You found nothing of interest.")
    
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """Handles discovering and adding new clues to the set."""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    return clues

def combat_encounter(player_stats, monster_health, has_treasure):
    """Simulates a combat encounter between the player and a monster."""
    while player_stats['health'] > 0 and monster_health > 0:
        print("You attack the monster!")
        monster_health -= player_stats['attack']
        if monster_health > 0:
            print("The monster fights back!")
            player_stats['health'] -= 10
    
    if player_stats['health'] > 0:
        print("You defeated the monster!")
        return has_treasure
    else:
        print("You have been defeated...")
        return None

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    for room in dungeon_rooms:
        room_name, item, challenge, challenge_data = room
        print(f"Entering {room_name}")
        
        if item:
            inventory.append(item)
            print(f"Found item: {item}")
        
        if challenge == "puzzle" or challenge == "trap":
            success, fail, penalty = challenge_data
            print(f"Encountered a {challenge}: {success} or {fail}")
            player_stats['health'] -= penalty
            
        if challenge == "library":
            clues_list = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(clues_list, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you understand the meaning of the clues and can bypass a puzzle challenge!")
    
    return player_stats, inventory, clues

def display_inventory(inventory):
    """Displays the player's inventory."""
    print("Inventory:", ", ".join(inventory))

def main():
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty Library", "key", "puzzle", ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow Passage, Creaky Floor", "torch", "trap", ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand Hall, Shimmering Pool", "healing potion", "none", None),
        ("Small Room, Locked Chest", "treasure", "puzzle", ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    
    artifacts = {
        "amulet_of_vitality": {
            "description": "A glowing amulet that enhances your life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "A powerful ring that boosts your attack damage.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "A staff imbued with ancient wisdom.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    
    has_treasure = random.choice([True, False])

    display_player_status(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        
        if treasure_obtained_in_combat:
            inventory.append("treasure")
        
        if random.random() < 0.3 and artifacts:
            artifact_name = random.choice(list(artifacts.keys()))
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
            display_player_status(player_stats)
        
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(player_stats, inventory, dungeon_rooms, clues)

    print("\n--- Game End ---")
    display_player_status(player_stats)
    print("Final Inventory:")
    display_inventory(inventory)
    print("Clues:")
    if clues:
        for clue in clues:
            print(f"- {clue}")
    else:
        print("No clues.")

if __name__ == "__main__":
    main()