#imports area
from random import choice, randint
from os import system, name

#consts area
ALL_SPECIALS = {'fireball':{'effect':'10 damage + d10 (FIRE)', 'uses':2},
                'firebolt':{'effect':'12 damage (FIRE)', 'uses':5},
                'grace':{'effect':'+3 health + d6 (GRASS)', 'uses':5},
                'sleep':{'effect':"d20 > 10 -> enemy can't act (GRASS)", 'uses':2}}
ELEMENT_REACTIONS = {'fire':['grass', 'ice'],
                     'grass':['rock']}

#classes area
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
        effect = ALL_SPECIALS[special]['effect']
        pp = ALL_SPECIALS[special]['uses']

        if pp > 0:
            ALL_SPECIALS[special]['uses'] -= 1

        if special in ALL_SPECIALS.keys() and pp > 0:
            print(f'{self.name} used {special}')

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
                        break
                
                other.health -= damage
                if other.health < 0:
                            other.health = 0

                print(f'{special} does {damage} damage!')

            elif 'health' in effect:
                healing = int(findall(r'\d+', effect)[0])
                print(f'heals for {healing} points!')
                self.health += healing
                if self.health > self.maxHealth:
                    self.health = self.maxHealth

class playerChar(char):
    def __init__(self, name, element, maxHealth, dmg, res, specials):
        super().__init__(name, element, maxHealth, dmg, res, specials)
        self.Level = 1
        self.XP = 0
        self.XPnextLevel = 50

    def levelUP(self):
        print(f'{self.name} leveld to level {self.Level}')
        self.XP = 0
        XPnextLevel *= 1,1
        self.Level += 1

        self.maxHealth += 10
        self.dmg += 5
        self.res += 1

        if len(self.specials) != len(list(ALL_SPECIALS.keys())):
            newSpecial = choice(list(ALL_SPECIALS.keys()))
            while newSpecial in self.specials:
                newSpecial = choice(list(ALL_SPECIALS.keys()))
            self.specials.append(newSpecial)
        
    
    def gainXP(self, amount:int):
        print(f'{self.name} gained {amount} XP!')
        self.XP += amount

        if self.XP >= self.XPnextLevel:
            self.XP -= self.XPnextLevel
            self.levelUP()
        
        print(f'current XP: {self.XP} || xp to next level: {self.XPnextLevel}')

#functions area
def okCheck():
    input('(press Enter)\n')

def randomEnemy(dif):
    enemyTipe = choice(list(ELEMENT_REACTIONS.keys()))
    specials = []

    if dif == 'easy':
        difMod = 1
    elif dif == 'medium':
        difMod = 3
    elif dif == 'hard':
        difMod = 5
    else:
        difMod = 10

    #caps number of spells enemy can have by the number of spells availible in gme
    for i in range(min(randint(0, difMod), len(ALL_SPECIALS) - len(specials))):
        spell = choice(list(ALL_SPECIALS.keys()))
        while spell in specials and enemyTipe.upper() not in spell:
            spell = choice(list(ALL_SPECIALS.keys()))
        specials.append(spell)
    
    return char('enemy', enemyTipe, randint(15, 20*difMod), randint(5, 7*difMod), randint(0, 3*difMod), specials)

# def debugEnemy(enemy:char, allActions:dict, toughts:dict, action:str):
#     print('ENEMY DEBUGGER !!!!!')
#     for s in enemy.specials:
#         print(f"{s} - {ALL_SPECIALS[s]['effect']}:{ALL_SPECIALS[s]['uses']}PP")
#     print(f'all actions: {allActions}\ntoughts: {toughts}\naction: {action}')

def enemyAI(enemy:char, player:char):
    possibleActions = {
        'attack':2,
    }
    for s in enemy.specials:
        possibleActions[s] = 5

    if 'grace' in possibleActions and enemy.health < enemy.maxHealth/2:
        possibleActions['grace'] = 2
    elif 'grace' in possibleActions and enemy.health > enemy.maxHealth/2:
        possibleActions['grace'] = 1
    else:
        pass
    
    from random import shuffle
    thought =[possibleAction for possibleAction, weight in possibleActions.items() for a in range(weight)]
    shuffle(thought)
    choosenAction = thought[0]
    
    if choosenAction == 'attack':
        enemy.attack(player)
    elif 'health' in ALL_SPECIALS[choosenAction]['effect']:
        enemy.use_special(choosenAction, enemy)
    elif 'damage' in ALL_SPECIALS[choosenAction]['effect']:
        enemy.use_special(choosenAction, player)
    
    #debugEnemy(enemy, possibleActions, thought, choosenAction)

def setWorldDif(playerLvl):
    if playerLvl == 1:
        dif = 'easy'
    elif playerLvl == 3:
        dif = 'medium'
    elif playerLvl == 5:
        dif = 'hard'
    elif playerLvl >= 7:
        dif == 'impossible'
    
    return dif

#-------------------------------main program running-------------------------------#

player = playerChar('Shy', 'fire', 100, 10, 2, [])

difficulty = setWorldDif(player.Level)
enemy1 = randomEnemy(difficulty)  

replay = ''
while replay != 'no' or 'n':
    while player.health and enemy1.health > 0:
        print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
        print(f'health: {player.health} || health: {enemy1.health} \n')

        moves = ['attack', 'special']
        print("actions:")
        for a in moves:
            if a != 'special' or len(player.specials) > 0:
                print(f"- {a}")

        
        while True:
            action = input('what will you do: ')
            match action:
                case 'attack':
                    player.attack(enemy1)
                    okCheck()
                    break
                case 'special' if len(player.specials) > 0:
                    print('specials list:')
                    for s in player.specials:
                        print(f"{s} - {ALL_SPECIALS[s]['effect']}:{ALL_SPECIALS[s]['uses']}PP")
                    player.use_special(input('choose the special: '), enemy1)
                    okCheck()
                    break
                case _:
                    print('invalid input !')
        
        print('-----------')
        print(f'{player.name} : {player.element} || {enemy1.name} : {enemy1.element}')
        print(f'health: {player.health} || health: {enemy1.health} \n')

        if enemy1.health > 0 and 'sleep' not in enemy1.status:
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

        xp = (enemy1.maxHealth + enemy1.dmg + enemy1.res) / 10
        player.gainXP(xp)

    #-----------------------------#

    replay = input('keep going (yes/no): ')
    while replay != 'yes' and 'no' and 'y' and 'n':
        replay = input('keep going (yes/no): ')
    
    print('A NEW FOE APPEARD !!!')
    player.health = player.maxHealth
        
    enemy1 = randomEnemy()

    system('cls' if name == 'nt' else 'clear')