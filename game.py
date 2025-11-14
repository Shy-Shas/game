from random import choice, randint

ALL_SPECIALS = {'fireball':'10 damage + d10', 'firebolt':'12 damage', 'grace':'+3 health + d6', 'sleep':" d20 > 10 -> enemy can't act"}
ELEMENT_REACTIONS = {'fire':['grass', 'ice'], 'grass':['rock']}

def okCheck():
    input('(press Enter)\n')

class dices:
    ALL_DICES = ['d6', 'd10', 'd20']

    def d6Roll():
        roll = randint(1, 7)
        print(f'd6 rolls a {roll}')
        return roll
    
    def d10Roll():
        roll = randint(1, 11)
        print(f'd6 rolls a {roll}')
        return roll
    
    def d20Roll():
        roll = randint(1, 21)
        print(f'd6 rolls a {roll}')
        return roll

class char:
    def __init__(self, name:str, element:str, maxHealth:int, dmg:int, res:int, specials:list):
        self.name = name
        self.element = element
        self.maxHealth = maxHealth
        self.dmg = dmg
        self.res = res
        self.specials = specials

        self.health = maxHealth
        self.status = []
        

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
            effect = ALL_SPECIALS[special]
            if 'damage' in effect:
                damage = int(findall(r'\d+', effect)[0])
                for dice in dices.ALL_DICES:
                    if dice in effect:
                        match dice:
                            case 'd20':
                                damage += dices.d20Roll()
                            case 'd10':
                                damage += dices.d10Roll()
                            case 'd6':
                                damage += dices.d6Roll()
                        print(f'{special} does {damage} damage!')
                        other.health -= damage
                        break
                else:
                    print(f'{special} does {damage} damage!')
                    other.health -= damage
            elif 'health' in effect:
                healing = int(findall(r'\d+', effect)[0])
                print(f'heals for {healing} points!')
                self.health += healing
                if self.health > self.maxHealth:
                    self.health = self.maxHealth

def randomEnemy():
    specials = []
    for i in range(randint(0,3)):
        spell = choice(list(ALL_SPECIALS.keys()))
        while spell in specials:
            spell = choice(list(ALL_SPECIALS.keys()))
        specials.append(spell)
    return char('enemy', choice(list(ELEMENT_REACTIONS.keys())), randint(15, 121), randint(5, 31), randint(0, 6), specials)

player = char('Shy', 'fire', 100, 10, 2, ['fireball', 'firebolt'])
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

    if enemy1.health <= 0 and 'sleep' not in enemy1.status:
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