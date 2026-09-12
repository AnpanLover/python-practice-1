# Text-based combat system
# with inventory system
# with smarter enemy
# OOP Refactoring version
import random

class Item:
    def __init__(self, name:str, quantity:int, using_type:int ,desc:str = " "):
        self.name = name
        self.desc = desc
        self.quantity = quantity
        # using type: is it using at item holder or at item holder's target
        # 0 = at item holder | 1 = at item holder's target
        self.using_type = using_type

class Healing_Potion(Item):
    def __init__(self, quantity:int, healing_amount:int):
        super().__init__(name="Healing Potion", quantity=quantity, using_type=0,desc=f"(Healing {healing_amount} HP.)")
        self.heal = healing_amount

    def using(self, target):
        target.hp += self.heal
        target.hp = min(target.hp, target.max_hp)
        print(f'Healing {target.name} by {self.heal} HP.')
        print(f"{target.name}'s HP: {target.hp}")

class Poison_Potion(Item):
    def __init__(self, quantity:int, damage_amount:int):
        super().__init__(name="Poison Potion", quantity=quantity, using_type=1,desc=f"(Dealing {damage_amount} Damage to an enemy.)")
        self.dmg = damage_amount

    def using(self, target):
        target.hp -= self.dmg
        target.hp = max(target.hp, 0)
        print(f"Dealing {self.dmg} damage to {target.name}.")
        print(f"{target.name}'s HP: {target.hp}")

class Character:
    def __init__(self, name, hp, max_hp):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp

class Player(Character):
    def __init__(self, name, hp, max_hp, atk_dmg:int):
        super().__init__(name, hp, max_hp)
        self.atk_dmg = atk_dmg
        self.target = None
        self.action = 0
        self.inventory = [
            Healing_Potion(2, 20),
            Poison_Potion(2, 20)
        ]

    def change_target(self, target):
        self.target = target

    def my_turn(self):
        div()
        print(f"[{self.name}'s turn]")
        print(f"HP: {self.hp}/{self.max_hp}")
        self.select_action()

    def input(self):
        while True:
            try:
                # take only postitve number
                self.action = abs(int(input("Select: ")))
                break
            except:
                print("* Invalid input (Number only)\n")

    def select_action(self):
        print("Select your action:")
        print(f"1. Attack (Deal {self.atk_dmg} damage to enemy.)")
        print("2. Inventory (Use an item.)")
        while True:
            self.input()
            match self.action:
                case 1:
                    div()
                    self.attack()
                    break
                case 2:
                    div()
                    self.open_inventory()
                    break
                case _:
                    print("* Invalid input (Must be 1 or 2)\n")

    def attack(self):
        if self.target.is_defending == False:
            self.target.hp -= self.atk_dmg
            self.target.hp = max(self.target.hp, 0)
            print(f"{self.name} Attacked {self.target.name}! Dealing {self.atk_dmg} damage.")
            print(f"{self.target.name}'s HP: {self.target.hp}")
        else:
            self.target.hp -= self.atk_dmg * 0.5
            self.target.hp = max(self.target.hp, 0)
            print(f"{self.name} Attacked {self.target.name}!")
            print(f"But {self.target.name} is defending, dealing {self.atk_dmg * 0.5} damage.")
            print(f"{self.target.name}'s HP: {self.target.hp}")

    def open_inventory(self):
        while True:
            print("--- Inventory ---")
            print("0. Close")
            for item in self.inventory:
                print(f'{self.inventory.index(item) + 1}. {item.name} x{item.quantity} | {item.desc}')
            self.input()
            match self.action:
                case 0:
                    div()
                    self.select_action()
                    break
                case _:
                    try:
                        div()
                        item = self.inventory[self.action - 1]
                        print(f'{self.name} used "{item.name}".\n')
                        # run item's func based on using type
                        match item.using_type:
                            case 0:
                                item.using(target = self)
                            case 1:
                                item.using(target = self.target)

                        item.quantity -= 1
                        print(f"\nYou have x{item.quantity} {item.name}  left.")
                        if item.quantity <= 0: self.inventory.remove(item)
                        break
                    except:
                        print("Invalid input: Item not found.\n")

class Normal_Monster(Character):
    def __init__(self, name, hp, max_hp, atk_dmg:int):
        super().__init__(name, hp, max_hp)
        self.atk_dmg = atk_dmg
        self.target = None
        self.action = 0
        self.is_defending = False

    def change_target(self, target):
        self.target = target

    def my_turn(self):
        div()
        print(f"[{self.name}'s turn]")

        # clear monster's defending state, so it wouldnt always defending
        self.is_defending = False

        # random monster's action
        # hp > 30% = attack = 60% | defend = 30% | heavy attack = 10%
        # hp < 30% = attack = 60% | heal = 40%
        action = random.randint(1,100)

        if self.hp > self.max_hp * 0.3:
            if action >= 1 and action <= 60: self.attack()
            if action >= 61 and action <= 90: self.defend()
            if action >= 91 and action <= 100: self.heavy_attack()
        else:
            if action >= 1 and action <= 60: self.attack()
            # healing itself by 15% to 30% of it's max HP
            if action >= 61 and action <= 100: self.heal(int( self.max_hp * random.uniform(0.15, 0.3) ) )

    def attack(self):
        self.target.hp -= self.atk_dmg
        self.target.hp = max(self.target.hp, 0)
        print(f"{self.name} Attacked {self.target.name}! Dealing {self.atk_dmg} damage.")
        print(f"{self.target.name}'s HP: {self.target.hp}")

    def heavy_attack(self):
        # just normal attack but x2 damage
        self.target.hp -= self.atk_dmg * 2
        self.target.hp = max(self.target.hp, 0)
        print(f"{self.name} use Heavy Attack at {self.target.name}! Dealing {self.atk_dmg * 2} damage.")
        print(f"{self.target.name}'s HP: {self.target.hp}")

    def heal(self, heal:int = 0):
        self.hp += heal
        self.hp = min(self.hp, self.max_hp)
        print(f'{self.name} Healing itself by {heal} HP.')
        print(f"{self.name}'s HP: {self.hp}")

    def defend(self):
        self.is_defending = True
        print(f"{self.name} is Defending | Reduce incoming damage by 50% for 1 turn.")

def div():
    print("--------------------")

# Main Function
p1 = Player("Newbie Adventurer", 100, 100, 15)
mon1 = Normal_Monster("Slime", 50, 50, 10)
p1.change_target(mon1)
mon1.change_target(p1)

print("=== Battle Start ===")
print(f"You encountered with: {mon1.name} | (HP:{mon1.hp} / ATK:{mon1.atk_dmg})")
print(f"You: {p1.name} | (HP:{p1.hp} / ATK:{p1.atk_dmg})")

while p1.hp > 0 and mon1.hp > 0:
    p1.my_turn()
    if mon1.hp <= 0: break
    mon1.my_turn()
    if p1.hp <= 0: break

div()
if mon1.hp <= 0 and p1.hp > 0:
    print("=== You won the battle ===")
elif mon1.hp > 0 and p1.hp <= 0:
    print("=== You lose the battle ===")
