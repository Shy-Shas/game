ALL_SPECIALS = {'fireball':'20 damage', 'grace':'+10 health', 'sleep':"enemy can't act"}
ELEMENT_REACTIONS = {'fire':['grass', 'ice'], 'grass':['rock']}

def okCheck():
    input('(press Enter)\n')

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
            other.health -= (self.dmg - other.res) * 2
            print(f'{self.name} attacked with {(self.dmg - other.res) * 2} damage!')
            if other.health < 0:
                other.health = 0
        else:
            other.health -= self.dmg - other.res
            print(f'{self.name} attacked with {self.dmg - other.res} damage!')
            if other.health < 0:
                other.health = 0
    
    def use_special(self, special, other):
        from re import findall
        if special in ALL_SPECIALS.keys():
            print(f'{self.name} used {special}')
            if 'damage' in ALL_SPECIALS[special]:
                damage = int(findall(r'\d+', ALL_SPECIALS[special])[0])
                print(f'{special} does {damage} damage!')
                other.health -= damage
            elif 'health' in ALL_SPECIALS[special]:
                healing = int(findall(r'\d+', ALL_SPECIALS[special])[0])
                print(f'heals for {healing} points!')
                self.health += healing
                if self.health > self.maxHealth:
                    self.health = self.maxHealth

def randomEnemy():
    from random import choice, randint
    specials = []
    for i in range(randint(0,3)):
        spell = choice(list(ALL_SPECIALS.keys()))
        while spell in specials:
            spell = choice(list(ALL_SPECIALS.keys()))
        specials.append(spell)
    return char('enemy', choice(list(ELEMENT_REACTIONS.keys())), randint(15, 120), randint(5, 30), randint(0, 5), specials)

player = char('Shy', 'fire', 100, 10, 2, ['fireball'])
enemy1 = randomEnemy()

def enemyAI(enemy:char, player:char):
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
            enemy.attack(player)
        case 'heal':
            enemy.use_special('grace', enemy)
    

while player.health and enemy1.health > 0:
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
                okCheck()
            case 'special':
                print('specials list:')
                for s in player.specials: print(f'{s} => {ALL_SPECIALS[s]}')
                player.use_special(input('choose the special: '), enemy1)
                okCheck()
            case _:
                print('invalid input !')
    
    print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
    print(f'health: {player.health} || health: {enemy1.health} \n')

    if enemy1.health <= 0:
        print('ENEMY TURN !')
        enemyAI(enemy1, player)
    okCheck()
    print('----------------------------------------\n')

print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
print(f'health: {player.health} || health: {enemy1.health} \n')

if player.health == 0:
    print('player looses !')
else:
    print('player wins !!!')