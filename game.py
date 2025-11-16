#imports area
from random import choice, randint
from os import system, name

#consts area
ALL_SPECIALS = {'fireball':{'effect':'10 damage + d10', 'type':'fire', 'uses':2},
                'firebolt':{'effect':'12 damage', 'type':'fire', 'uses':5},
                'grace':{'effect':'+3 health + d6', 'type':'grass', 'uses':5},
                'sleep':{'effect':"d20  min10 -> enemy sleeps for 1 turn", 'type':'grass', 'uses':2}}

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
        print(f'd10 rolls a {roll}')
        return roll
    
    def d20Roll():
        roll = randint(1, 21)
        print(f'd20 rolls a {roll}')
        return roll

class char:
    def __init__(self, name:str, element:str, maxHealth:int, dmg:int, res:int, specials:dict):
        self.name = name
        self.element = element
        self.maxHealth = maxHealth
        self.dmg = dmg
        self.res = res
        self.specials = specials

        self.health = maxHealth
        self.status = []

    def canAct(self):
        if 'sleep' in self.status:
            return False
        else:
            return True

    def attack(self, other):
        if self.canAct():
            if other.element in ELEMENT_REACTIONS[self.element]:
                print('BONUS ELEMENTAL DAMAGE!')
                damage = (dices.d6Roll() + self.dmg - other.res) * 2
                other.health -= damage
                print(f'{self.name} attacked with {damage} damage!')
                if other.health < 0:
                    other.health = 0
            else:
                damage = dices.d6Roll() + self.dmg - other.res
                other.health -= damage
                print(f'{self.name} attacked with {damage} damage!')
                if other.health < 0:
                    other.health = 0
    
    def use_special(self, special, other):
        if self.canAct():
            from re import findall
            effect = ALL_SPECIALS[special]['effect']
            pp = self.specials[special]

            if pp > 0:
                self.specials[special] -= 1

            if special in ALL_SPECIALS.keys() and pp > 0:
                print(f'{self.name} used {special}')

                if 'damage' in effect:
                    damage = int(findall(r'\d+', effect)[0])
                    element = ALL_SPECIALS[special]['type']

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
                    
                    if element in ELEMENT_REACTIONS[element]:
                        damage *= 2

                    other.health -= damage
                    if other.health < 0:
                                other.health = 0

                    print(f'{special} does {damage} damage!')

                elif 'health' in effect:
                    healing = int(findall(r'\d+', effect)[0])
                    print(f'heals for {healing} points!')

                    for dice in dices.ALL_DICES:
                        if dice in effect:
                            match dice:
                                case 'd20':
                                    healing += dices.d20Roll()
                                case 'd10':
                                    healing += dices.d10Roll()
                                case 'd6':
                                    healing += dices.d6Roll() 
                            break

                    self.health += healing
                    if self.health > self.maxHealth:
                        self.health = self.maxHealth

                elif 'sleeps' in effect:
                    minRoll = int(findall(r'\d+', effect)[1])
                    roll = 0

                    duration = int(findall(r'\d+', effect)[2])

                    for dice in dices.ALL_DICES:
                        if dice in effect:
                            match dice:
                                case 'd20':
                                    roll= dices.d20Roll()
                                case 'd10':
                                    roll= dices.d10Roll()
                                case 'd6':
                                    roll= dices.d6Roll() 
                            break

                    if roll >= minRoll:
                        for i in range(duration):
                            other.status.append('sleep')
                        print(f'{other.name} fell asleep!')
                    else:
                        print(f'{self.name} missed the spell !')

    def removeStatus(self):
        statusList = self.status
        if not self.canAct():
            statusList.remove('sleep')

            if 'sleep' in statusList:
                print(f'{self} is still sleeping!')
            else:
                print(f'{self.name} woke up!')


class playerChar(char):
    def __init__(self, name, element, maxHealth, dmg, res, specials):
        super().__init__(name, element, maxHealth, dmg, res, specials)
        self.Level = 1
        self.XP = 0
        self.XPnextLevel = 50

    def levelUP(self):
        self.XPnextLevel = round(self.XPnextLevel * 1.1)
        self.Level += 1

        self.maxHealth += 10
        self.dmg += 5
        self.res += 1

        print(f'{self.name} leveld to level {self.Level}')

        if len(self.specials) != len(list(ALL_SPECIALS.keys())):
            newSpecial = choice(list(ALL_SPECIALS.keys()))
            while newSpecial in self.specials.keys():
                newSpecial = choice(list(ALL_SPECIALS.keys()))
            self.specials[newSpecial] = ALL_SPECIALS[newSpecial]['uses']
        
            print(f'learnded new spell: {newSpecial} !')
        
    
    def gainXP(self, amount:int):
        print(f'{self.name} gained {amount} XP!')
        self.XP += amount
        print(f'current XP: {self.XP} || xp to next level: {self.XPnextLevel}')

        while self.XP >= self.XPnextLevel:
            self.XP -= self.XPnextLevel
            self.levelUP()
            print(f'current XP: {self.XP} || xp to next level: {self.XPnextLevel}')
        

#functions area
def okCheck():
    input('(press Enter)\n')

def randomEnemy(dif):
    enemyTipe = choice(list(ELEMENT_REACTIONS.keys()))
    specials = {}

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
        specials[spell] = ALL_SPECIALS[spell]['uses']
    
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
    for s in enemy.specials.keys():
        possibleActions[s] = 1

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

#----------------------------------------------------------------------------------#
#-------------------------------main program running-------------------------------#
#----------------------------------------------------------------------------------#

player = playerChar('Shy', 'fire', 100, 10, 2, {'sleep':2})

difficulty = setWorldDif(player.Level)
enemy = randomEnemy(difficulty)  



running = True
while running:
    while player.health and enemy.health > 0:

        print(f'{player.name} : {player.element} || {enemy.name} : {enemy.element}')
        print(f'health: {player.health} || health: {enemy.health} \n')

        player.removeStatus()

        while True:
            if player.canAct():
                moves = ['attack', 'special', 'info']
                print("actions:")
                for a in moves:
                    if a != 'special' or len(player.specials) > 0:
                        print(f"- {a}")

                action = input('what will you do: ')
                match action:
                    case 'attack':
                        player.attack(enemy)
                        okCheck()
                        break
                    case 'special' if len(player.specials) > 0:
                        print('specials list:')
                        for s in player.specials:
                            print(f"{s} - {ALL_SPECIALS[s]['effect']} : {player.specials[s]}PP")
                        while True:
                            choosenSpell = input('choose the special: ')
                            if player.specials[choosenSpell] > 0:
                                break
                            else:
                                ('The spell has no PP left !!!')
                        player.use_special(choosenSpell, enemy)
                        okCheck()
                        break
                    case 'info':
                        print(player.name)
                        print(f'element: {player.element} | Level: {player.Level}')
                        print(f'Current XP: {player.XP} | XP to next level: {player.XPnextLevel}')
                        print(f'health: {player.health}\ndamage: {player.dmg}\nresistance: {player.res}')
                        print('specials:')
                        for s in player.specials:
                            print(f'-{s} ->\n'
                                f"  effect: {ALL_SPECIALS[s]['effect']}\n"
                                f"  type: {ALL_SPECIALS[s]['type']}"
                                f"  PP: {ALL_SPECIALS[s]['uses']}\n")
                    case _:
                        print('invalid input !')
        
        print('-----------')
        print(f'{player.name} : {player.element} || {enemy.name} : {enemy.element}')
        print(f'health: {player.health} || health: {enemy.health} \n')

        if enemy.health > 0 and enemy.canAct():
            print('ENEMY TURN !')
            enemyAI(enemy, player)
        elif not enemy.canAct():
            print(f'{enemy.name} is sleeping!')

        okCheck()
        if len(enemy.status) > 0:
            enemy.removeStatus()
            okCheck()
        print('----------------------------------------\n')

    print(f'{player.name} : {player.element} || {enemy.name} : {enemy.element}')
    print(f'health: {player.health} || health: {enemy.health} \n')

    if player.health == 0:
        print('player looses !')
    else:
        print('player wins !!!')

        xp = enemy.maxHealth + enemy.dmg + enemy.res
        player.gainXP(xp)

    #-----------------------------#

    while True:
        replay = input('keep going (yes/no): ')
        match replay:
            case 'yes' | 'y' | '':
                print('A NEW FOE APPEARD !!!')
                okCheck()
                player.health = player.maxHealth
                for s in player.specials:
                    player.specials[s] = ALL_SPECIALS[s]['uses']
                    
                enemy1 = randomEnemy(difficulty)

                system('cls' if name == 'nt' else 'clear')
                break
            case 'no' | 'n':
                running = False
                break
            case _:
                print('Unhandled answer, please tipe again !')
    