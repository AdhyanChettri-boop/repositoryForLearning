import random
import time
import os
import json

# ==========================================
# EPIC TERMINAL WORLD
# Large single-file Python project for GitHub
# ==========================================


# ---------- Utility ----------


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')



def slow_print(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# ---------- Data ----------

ENEMY_TYPES = [
    {
        'name': 'Goblin',
        'hp': 30,
        'attack': 5,
        'gold': 10,
        'xp': 15
    },
    {
        'name': 'Skeleton',
        'hp': 40,
        'attack': 8,
        'gold': 18,
        'xp': 25
    },
    {
        'name': 'Orc',
        'hp': 60,
        'attack': 12,
        'gold': 30,
        'xp': 45
    },
    {
        'name': 'Shadow Knight',
        'hp': 90,
        'attack': 18,
        'gold': 60,
        'xp': 80
    }
]

ITEMS = {
    'Small Potion': 25,
    'Large Potion': 60,
    'Iron Sword': 120,
    'Steel Armor': 180,
    'Magic Ring': 250
}

LOCATIONS = [
    'Ancient Forest',
    'Crystal Cave',
    'Dark Dungeon',
    'Forgotten Temple',
    'Abandoned Village',
    'Frozen Mountain',
    'Burning Desert',
    'Ruined Castle'
]

QUESTS = [
    'Defeat 3 Goblins',
    'Collect 100 Gold',
    'Find the Lost Relic',
    'Reach Level 5',
    'Survive the Dungeon',
    'Defeat the Shadow Knight'
]


# ---------- Classes ----------

class Player:

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.xp = 0
        self.inventory = []
        self.location = 'Town'
        self.quests = []
        self.kills = 0
        self.steps = 0

    def show_stats(self):
        print('\n========== PLAYER STATS ==========' )
        print(f'Name      : {self.name}')
        print(f'Level     : {self.level}')
        print(f'HP        : {self.hp}/{self.max_hp}')
        print(f'Attack    : {self.attack}')
        print(f'Defense   : {self.defense}')
        print(f'Gold      : {self.gold}')
        print(f'XP        : {self.xp}')
        print(f'Kills     : {self.kills}')
        print(f'Steps     : {self.steps}')
        print(f'Location  : {self.location}')
        print('==================================')

    def gain_xp(self, amount):
        self.xp += amount
        needed = self.level * 100

        if self.xp >= needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 25
        self.attack += 4
        self.defense += 2
        self.hp = self.max_hp

        print('\n*** LEVEL UP! ***')
        print(f'You are now level {self.level}!')

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def take_damage(self, amount):
        reduced = amount - self.defense

        if reduced < 1:
            reduced = 1

        self.hp -= reduced

        print(f'{self.name} took {reduced} damage!')

    def add_item(self, item):
        self.inventory.append(item)
        print(f'Added {item} to inventory.')

    def show_inventory(self):
        print('\n========== INVENTORY ==========' )

        if not self.inventory:
            print('Inventory is empty.')
        else:
            for i, item in enumerate(self.inventory, start=1):
                print(f'{i}. {item}')

        print('================================')


class Enemy:

    def __init__(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.attack = data['attack']
        self.gold = data['gold']
        self.xp = data['xp']

    def take_damage(self, amount):
        self.hp -= amount


# ---------- Saving ----------


def save_game(player):
    data = {
        'name': player.name,
        'level': player.level,
        'hp': player.hp,
        'max_hp': player.max_hp,
        'attack': player.attack,
        'defense': player.defense,
        'gold': player.gold,
        'xp': player.xp,
        'inventory': player.inventory,
        'location': player.location,
        'quests': player.quests,
        'kills': player.kills,
        'steps': player.steps
    }

    with open('savegame.json', 'w') as file:
        json.dump(data, file)

    print('Game saved successfully.')



def load_game():
    try:
        with open('savegame.json', 'r') as file:
            data = json.load(file)

        player = Player(data['name'])

        player.level = data['level']
        player.hp = data['hp']
        player.max_hp = data['max_hp']
        player.attack = data['attack']
        player.defense = data['defense']
        player.gold = data['gold']
        player.xp = data['xp']
        player.inventory = data['inventory']
        player.location = data['location']
        player.quests = data['quests']
        player.kills = data['kills']
        player.steps = data['steps']

        print('Save loaded successfully.')
        return player

    except FileNotFoundError:
        print('No save file found.')
        return None


# ---------- Exploration ----------


def explore(player):
    clear_screen()

    location = random.choice(LOCATIONS)
    player.location = location
    player.steps += 1

    slow_print(f'You travel to {location}...')

    event = random.randint(1, 5)

    if event == 1:
        find_gold(player)

    elif event == 2:
        battle(player)

    elif event == 3:
        discover_item(player)

    elif event == 4:
        mysterious_event(player)

    else:
        peaceful_event(player)


# ---------- Events ----------


def find_gold(player):
    amount = random.randint(10, 100)
    player.gold += amount

    print(f'You found {amount} gold!')



def discover_item(player):
    item = random.choice(list(ITEMS.keys()))
    player.add_item(item)



def mysterious_event(player):
    print('A mysterious traveler approaches you...')

    outcome = random.randint(1, 3)

    if outcome == 1:
        player.heal(30)
        print('The traveler healed you.')

    elif outcome == 2:
        stolen = min(player.gold, 25)
        player.gold -= stolen
        print(f'The traveler stole {stolen} gold!')

    else:
        player.attack += 1
        print('The traveler trained you. Attack increased!')



def peaceful_event(player):
    print('The area is peaceful today.')
    print('You rest beside a campfire.')

    player.heal(15)


# ---------- Combat ----------


def battle(player):
    enemy_data = random.choice(ENEMY_TYPES)
    enemy = Enemy(enemy_data)

    print(f'\nA wild {enemy.name} appeared!')

    while enemy.hp > 0 and player.hp > 0:

        print('\n========== BATTLE ==========' )
        print(f'{enemy.name} HP: {enemy.hp}')
        print(f'{player.name} HP: {player.hp}/{player.max_hp}')
        print('============================')

        print('1. Attack')
        print('2. Use Potion')
        print('3. Run')

        choice = input('Choose: ')

        if choice == '1':
            damage = player.attack + random.randint(1, 6)
            enemy.take_damage(damage)

            print(f'You dealt {damage} damage!')

        elif choice == '2':
            use_potion(player)

        elif choice == '3':
            escape = random.randint(1, 2)

            if escape == 1:
                print('You escaped successfully.')
                return
            else:
                print('Escape failed!')

        else:
            print('Invalid choice.')
            continue

        if enemy.hp > 0:
            player.take_damage(enemy.attack)

    if player.hp <= 0:
        game_over(player)

    else:
        print(f'You defeated the {enemy.name}!')

        player.gold += enemy.gold
        player.gain_xp(enemy.xp)
        player.kills += 1

        print(f'+{enemy.gold} gold')
        print(f'+{enemy.xp} XP')


# ---------- Inventory ----------


def use_potion(player):
    if 'Small Potion' in player.inventory:
        player.inventory.remove('Small Potion')
        player.heal(30)
        print('Used Small Potion.')

    elif 'Large Potion' in player.inventory:
        player.inventory.remove('Large Potion')
        player.heal(60)
        print('Used Large Potion.')

    else:
        print('No potions available.')


# ---------- Shop ----------


def shop(player):

    while True:
        print('\n========== SHOP ==========' )
        print(f'Gold: {player.gold}')
        print('==========================')

        for i, item in enumerate(ITEMS, start=1):
            print(f'{i}. {item} - {ITEMS[item]} gold')

        print('0. Exit Shop')

        choice = input('Choose item: ')

        if choice == '0':
            break

        try:
            index = int(choice) - 1
            item_name = list(ITEMS.keys())[index]
            price = ITEMS[item_name]

            if player.gold >= price:
                player.gold -= price
                player.add_item(item_name)

                if item_name == 'Iron Sword':
                    player.attack += 5

                elif item_name == 'Steel Armor':
                    player.defense += 4

                elif item_name == 'Magic Ring':
                    player.max_hp += 20
                    player.hp = player.max_hp

                print('Purchase successful.')

            else:
                print('Not enough gold.')

        except:
            print('Invalid selection.')


# ---------- Quests ----------


def quest_board(player):

    while True:
        print('\n========== QUEST BOARD ==========' )

        for i, quest in enumerate(QUESTS, start=1):
            print(f'{i}. {quest}')

        print('0. Exit')

        choice = input('Accept quest: ')

        if choice == '0':
            break

        try:
            quest = QUESTS[int(choice) - 1]

            if quest not in player.quests:
                player.quests.append(quest)
                print(f'Accepted quest: {quest}')
            else:
                print('Quest already active.')

        except:
            print('Invalid quest.')



def show_quests(player):
    print('\n========== ACTIVE QUESTS ==========' )

    if not player.quests:
        print('No active quests.')

    else:
        for quest in player.quests:
            print(f'- {quest}')


# ---------- Mini Games ----------


def dice_game(player):
    print('\nWelcome to Dice Duel!')

    bet = input('Enter gold to bet: ')

    try:
        bet = int(bet)

        if bet <= 0:
            return

        if bet > player.gold:
            print('Not enough gold.')
            return

        player_roll = random.randint(1, 6)
        enemy_roll = random.randint(1, 6)

        print(f'You rolled {player_roll}')
        print(f'Enemy rolled {enemy_roll}')

        if player_roll > enemy_roll:
            player.gold += bet
            print(f'You won {bet} gold!')

        elif player_roll < enemy_roll:
            player.gold -= bet
            print(f'You lost {bet} gold!')

        else:
            print('Draw.')

    except:
        print('Invalid amount.')



def guessing_game(player):
    number = random.randint(1, 20)

    print('\nGuess the Number!')
    print('Guess a number between 1 and 20.')

    tries = 5

    while tries > 0:
        guess = input('Your guess: ')

        try:
            guess = int(guess)

            if guess == number:
                reward = 50
                player.gold += reward

                print(f'Correct! You earned {reward} gold.')
                return

            elif guess < number:
                print('Too low.')

            else:
                print('Too high.')

            tries -= 1
            print(f'Tries left: {tries}')

        except:
            print('Invalid number.')

    print(f'You lost. The number was {number}.')


# ---------- Achievements ----------


def achievements(player):
    print('\n========== ACHIEVEMENTS ==========' )

    if player.level >= 5:
        print('✔ Experienced Adventurer')

    if player.gold >= 500:
        print('✔ Wealth Collector')

    if player.kills >= 10:
        print('✔ Monster Hunter')

    if player.steps >= 20:
        print('✔ Explorer')

    if player.level < 5 and player.gold < 500 and player.kills < 10 and player.steps < 20:
        print('No achievements unlocked yet.')


# ---------- Arena ----------


def arena(player):
    print('\n========== ARENA ==========' )
    print('Fight endless enemies for rewards.')

    wins = 0

    while True:
        enemy_data = random.choice(ENEMY_TYPES)
        enemy = Enemy(enemy_data)

        print(f'\nArena Enemy: {enemy.name}')

        while enemy.hp > 0 and player.hp > 0:
            damage = player.attack + random.randint(1, 10)
            enemy.take_damage(damage)

            print(f'You hit {enemy.name} for {damage}')

            if enemy.hp > 0:
                player.take_damage(enemy.attack)

        if player.hp <= 0:
            print('Arena defeat!')
            player.hp = player.max_hp
            break

        wins += 1
        reward = wins * 25
        player.gold += reward

        print(f'Victory! Reward: {reward} gold')

        cont = input('Continue arena? (y/n): ')

        if cont.lower() != 'y':
            break


# ---------- Crafting ----------


def crafting(player):
    print('\n========== CRAFTING ==========' )
    print('1. Craft Mega Potion')
    print('2. Craft Fire Blade')
    print('3. Exit')

    choice = input('Choose: ')

    if choice == '1':
        if player.inventory.count('Small Potion') >= 2:
            player.inventory.remove('Small Potion')
            player.inventory.remove('Small Potion')
            player.inventory.append('Mega Potion')
            print('Crafted Mega Potion!')

        else:
            print('Need 2 Small Potions.')

    elif choice == '2':
        if 'Iron Sword' in player.inventory:
            player.inventory.append('Fire Blade')
            player.attack += 10
            print('Crafted Fire Blade!')

        else:
            print('Need Iron Sword.')


# ---------- Boss Fight ----------


def boss_fight(player):
    print('\n========== FINAL BOSS ==========' )

    boss = Enemy({
        'name': 'Ancient Dragon',
        'hp': 250,
        'attack': 25,
        'gold': 500,
        'xp': 300
    })

    while boss.hp > 0 and player.hp > 0:
        print(f'Boss HP: {boss.hp}')
        print(f'Your HP: {player.hp}/{player.max_hp}')

        print('1. Attack')
        print('2. Heal')

        choice = input('Choose: ')

        if choice == '1':
            damage = player.attack + random.randint(5, 15)
            boss.take_damage(damage)
            print(f'You dealt {damage} damage!')

        elif choice == '2':
            use_potion(player)

        if boss.hp > 0:
            player.take_damage(boss.attack)

    if player.hp <= 0:
        print('The Ancient Dragon defeated you...')

    else:
        print('YOU DEFEATED THE ANCIENT DRAGON!')
        player.gold += boss.gold
        player.gain_xp(boss.xp)


# ---------- Game Over ----------


def game_over(player):
    print('\n========== GAME OVER ==========' )
    print(f'{player.name} has fallen.')
    print(f'Level Reached : {player.level}')
    print(f'Gold Collected: {player.gold}')
    print(f'Enemies Killed: {player.kills}')
    print('================================')

    exit()


# ---------- Main Menu ----------


def main_menu(player):

    while True:
        print('\n========== MAIN MENU ==========' )
        print('1. Explore')
        print('2. Stats')
        print('3. Inventory')
        print('4. Shop')
        print('5. Quest Board')
        print('6. Active Quests')
        print('7. Dice Game')
        print('8. Guessing Game')
        print('9. Achievements')
        print('10. Arena')
        print('11. Crafting')
        print('12. Boss Fight')
        print('13. Save Game')
        print('14. Exit')

        choice = input('Choose option: ')

        if choice == '1':
            explore(player)

        elif choice == '2':
            player.show_stats()

        elif choice == '3':
            player.show_inventory()

        elif choice == '4':
            shop(player)

        elif choice == '5':
            quest_board(player)

        elif choice == '6':
            show_quests(player)

        elif choice == '7':
            dice_game(player)

        elif choice == '8':
            guessing_game(player)

        elif choice == '9':
            achievements(player)

        elif choice == '10':
            arena(player)

        elif choice == '11':
            crafting(player)

        elif choice == '12':
            boss_fight(player)

        elif choice == '13':
            save_game(player)

        elif choice == '14':
            print('Thanks for playing!')
            break

        else:
            print('Invalid option.')


# ---------- Intro ----------


def intro():
    clear_screen()

    print('========================================')
    print('        EPIC TERMINAL WORLD')
    print('========================================')

    print('1. New Game')
    print('2. Load Game')
    print('3. Exit')


# ---------- Main ----------


def main():

    while True:
        intro()

        choice = input('Choose: ')

        if choice == '1':
            name = input('Enter your hero name: ')
            player = Player(name)
            main_menu(player)

        elif choice == '2':
            player = load_game()

            if player:
                main_menu(player)

        elif choice == '3':
            print('Goodbye.')
            break

        else:
            print('Invalid option.')


# ---------- Launch ----------

if __name__ == '__main__':
    main()
