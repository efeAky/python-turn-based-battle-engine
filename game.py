import random
from abc import ABC, abstractmethod

# Base class for all characters
class Character:
    def __init__(self, name: str, health: int, attack_power: int, defense: int, cooldown: int):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.cooldown = cooldown  # Negative countdown for special move

    # Apply damage from an attacker
    def take_damage(self, attacker):
        total_damage = max(0, attacker.attack_power - self.defense)
        if total_damage == 0:
            print(f"{self.name} fully counters the attack!")
            print(f"{self.name}'s health: {self.health}\n")
        else:
            self.health -= total_damage
            if self.health <= 0:
                self.health = 0
                print(f"{self.name} takes {total_damage} damage and dies!\n")
            else:
                print(f"{self.name} counters {self.defense} points!")
                print(f"{self.name}'s health: {self.health}\n")

    # Check if character is alive
    def is_alive(self):
        return self.health > 0

    # Countdown for special move each turn
    def reduce_cooldown(self):
        if self.cooldown < 0:
            self.cooldown += 1
        return self.cooldown

# Abstract class for normal attacks
class Attackable(ABC):
    @abstractmethod
    def attack(self, target):
        pass

# Abstract class for special moves
class SpecialMove(ABC):
    @abstractmethod
    def use_special_move(self, target):
        pass

# Warrior character class
class Warrior(Character, Attackable, SpecialMove):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=25, defense=15, cooldown=-3)

    # Normal attack implementation
    def attack(self, target):
        print(f"{self.name} swings a mighty sword at {target.name} with {self.attack_power} damage points!")
        target.take_damage(self)

    # Special move implementation
    def use_special_move(self, target):
        if self.cooldown == 0:  # Only usable if countdown reached 0
            original_attack = self.attack_power
            self.attack_power += 15
            print(f"{self.name} uses MIGHTY STRIKE with {self.attack_power} damage points on {target.name}!")
            target.take_damage(self)
            self.attack_power = original_attack
            self.cooldown = -3  # Reset cooldown

# Mage character class
class Mage(Character, Attackable, SpecialMove):
    def __init__(self, name):
        super().__init__(name, health=70, attack_power=35, defense=5, cooldown=-4)

    def attack(self, target):
        print(f"{self.name} casts a powerful spell at {target.name} with {self.attack_power} damage points!")
        target.take_damage(self)

    def use_special_move(self, target):
        if self.cooldown == 0:
            original_attack = self.attack_power
            self.attack_power += 20
            print(f"{self.name} uses ARCANE BLAST with {self.attack_power} damage points on {target.name}!")
            target.take_damage(self)
            self.attack_power = original_attack
            self.cooldown = -4

# Orc enemy class
class Orc(Character, Attackable, SpecialMove):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30, defense=10, cooldown=-3)

    def attack(self, target):
        print(f"{self.name} smashes {target.name} with brute force for {self.attack_power} damage points!")
        target.take_damage(self)

    def use_special_move(self, target):
        if self.cooldown == 0:
            original_attack = self.attack_power
            self.attack_power += 18
            print(f"{self.name} uses BERSERKER RAGE with {self.attack_power} damage points on {target.name}!")
            target.take_damage(self)
            self.attack_power = original_attack
            self.cooldown = -3

# Goblin enemy class
class Goblin(Character, Attackable, SpecialMove):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=20, defense=8, cooldown=-2)

    def attack(self, target):
        print(f"{self.name} throws its spear at {target.name} for {self.attack_power} damage points!")
        target.take_damage(self)

    def use_special_move(self, target):
        if self.cooldown == 0:
            original_attack = self.attack_power
            self.attack_power += 12
            print(f"{self.name} uses POISON DART with {self.attack_power} damage points on {target.name}!")
            target.take_damage(self)
            self.attack_power = original_attack
            self.cooldown = -2

# Battle function: turn-based system
def battle(fighter1, fighter2):
    print(f"{fighter1.name} VS {fighter2.name}")
    turn = random.randint(0, 1)  # Random first turn
    while fighter1.is_alive() and fighter2.is_alive():
        if turn % 2 == 0:
            if fighter1.cooldown == 0:
                fighter1.use_special_move(fighter2)
            else:
                fighter1.attack(fighter2)
            fighter1.reduce_cooldown()  # Reduce cooldown each turn
        else:
            if fighter2.cooldown == 0:
                fighter2.use_special_move(fighter1)
            else:
                fighter2.attack(fighter1)
            fighter2.reduce_cooldown()
        turn += 1

    # Announce winner
    if fighter1.is_alive():
        print(f"{fighter1.name} wins the fight!")
    else:
        print(f"{fighter2.name} wins the fight!")
    print("*******************\n")

# Create characters
hero1 = Warrior("Warrior")
hero2 = Mage("Mage")
enemy1 = Orc("Orc")
enemy2 = Goblin("Goblin")

# Dictionary for easy selection
all_characters = {
    "warrior": hero1,
    "mage": hero2,
    "orc": enemy1,
    "goblin": enemy2
}

# Display character stats
def show_stats(char_list):
    print("Available characters:")
    for char in char_list:
        print(f"{char.name}: Health={char.health}, Attack={char.attack_power}, Defense={char.defense}")

# Hero selection
show_stats([hero1, hero2])
while True:
    hero_name = input("Enter hero name: ").strip().lower()  # lowercase and remove spaces
    if hero_name in ["warrior", "mage"]:
        selected_hero = all_characters[hero_name]
        print(f"You selected: {selected_hero.name}\n")
        break
    print("Invalid hero. Try again.")

# Enemy selection
show_stats([enemy1, enemy2])
while True:
    enemy_name = input("Enter enemy name: ").strip().lower()  # lowercase and remove spaces
    if enemy_name in ["orc", "goblin"]:
        selected_enemy = all_characters[enemy_name]
        print(f"You selected: {selected_enemy.name}\n")
        break
    print("Invalid enemy. Try again.")


# Start the battle
battle(selected_hero, selected_enemy)
