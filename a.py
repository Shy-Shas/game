ALL_SPECIALS = {'fireball':'20 damage', 'grace':'+10 health', 'sleep':"enemy can't act"}
ELEMENT_REACTIONS = {'fire':['grass', 'ice'], 'grass':['rock']}

class char:
    def __init__(self, name:str, element:str, maxHealth:int, dmg:int, res:int, specials:list):
        self.name = name
        self.element = element
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.dmg = dmg
        self.res = res
        self.specials = specials
        

    def attack(self, other):
        if other.element in ELEMENT_REACTIONS[self.element]:
            print('BONUS ELEMENTAL DAMAGE!')
            other.health -= self.dmg * 2
            if other.health < 0:
                other.health = 0
        else:
            other.health -= self.dmg - other.res
            if other.health < 0:
                other.health = 0
    
    def die(self):
        return print(f"{self.name} has died!")
    
    def use_special(self, special, other):
        from re import findall
        if special in ALL_SPECIALS.keys():
            if 'damage' in ALL_SPECIALS[special]:
                other.health -= int(findall(r'\d+', ALL_SPECIALS[special])[0])
            elif 'health' in ALL_SPECIALS[special]:
                self.health += int(findall(r'\d+', ALL_SPECIALS[special])[0])

player = char('Shy', 'fire', 100, 10, 2, ['fireball'])

enemy1 = char('Enemy', 'grass', 40, 5, 1, ['heal'])

def enemy_turn(enemy:char, player:char):
    possibleActions = {
        'attack':2,
        'heal':1
    }

    if enemy.health < enemy.maxHealth/2:
        possibleActions['heal'] = 3
    else:
        possibleActions['heal'] = 1
    
    from random import shuffle
    thought =[possibleAction for possibleAction, weight in possibleActions.items() for a in range(weight)]
    shuffle(thought)
    choosenAction = thought[0]
    
    match choosenAction:
        case 'attack':
            print(f'enemy attacks for {enemy.dmg - player.res} damage !')
            enemy.attack(player)
        case 'heal':
            print('enemy heals !')
            enemy.use_special('heal', enemy)
    

while player.health and enemy1.health > 0:
    from time import sleep
    print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
    print(f'health: {player.health} || health: {enemy1.health} \n')

    ACTIONS = ['attack', 'special']
    print("actions:")
    for a in ACTIONS:
        print(f"- {a}")
    
    action = ''
    while action not in ACTIONS:
        action = input('what will you do: ')
        match action:
            case 'attack':
                player.attack(enemy1)
                print(f'player attacked for {player.dmg - enemy1.res}')
                sleep(0.5)
            case 'special':
                for s in player.specials: print(f'{s} => {ALL_SPECIALS[s]}')
                player.use_special(input('choose the special: '), enemy1)
                sleep(0.5)
            case _:
                print('invalid input !')
    
    print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
    print(f'health: {player.health} || health: {enemy1.health} \n')

    print('ENEMY TURN !')
    enemy_turn(enemy1, player)
    sleep(1)
    print('----------------------------------------\n')

print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
print(f'health: {player.health} || health: {enemy1.health} \n')

if player.health == 0:
    print('player looses !')
else:
    print('player wins !!!')