#imports area
from random import choice, randint
from os import system, name

import spellsFunctions
import itemsFile

#consts area
ALL_SPECIALS = spellsFunctions.SPECIALS

ELEMENT_REACTIONS = spellsFunctions.REACTIONS

ITEMS_LIST = itemsFile.ITEMS_DICT

#classes area
dices = spellsFunctions.dices

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
        self.inv:dict = {}

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
            else:
                damage = dices.d6Roll() + self.dmg - other.res
                other.health -= damage
                print(f'{self.name} attacked with {damage} damage!')
            
            other.correctHealth()
            self.correctHealth()
    
    def use_special(self, special, other):
        if self.canAct():
            pp = self.specials[special]

            if pp > 0:
                self.specials[special] -= 1

            if special in ALL_SPECIALS.keys() and pp > 0:
                print(f'{self.name} used {special}')

                match special:
                    case 'fireball':
                        spellsFunctions.fireball(other)
                    case 'firebolt':
                        spellsFunctions.firebolt(other)
                    case 'lava ground':
                        spellsFunctions.lavaGround(self.name, other)
                    case 'grace':
                        spellsFunctions.grace(self)
                    case 'sleep':
                        spellsFunctions.sleep(self.name, other)
                    case 'thorn rain':
                        spellsFunctions.thornRain(other)
            
            other.correctHealth()
            self.correctHealth()

    def useItemDef( self, item):
        itemsFile.item.useItem(item, self)

    def updateStatus(self):
        sl = self.status
        if len(sl) > 0:
            if 'sleep' in sl:
                sl.remove('sleep')

                if 'sleep' in sl:
                    print(f'{self.name} is still sleeping!')
                else:
                    print(f'{self.name} woke up!')
            
            if 'burn' in sl:
                self.health -= 7
                print(f'{self.name} takes 2 damage from burn!')
                sl.remove('burn')

                if 'burn' in sl:
                    print(f'{self.name} is still burning!')
                else:
                    print(f'{self.name} is not burning anymore!')

    def correctHealth(self):
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        
        if self.health < 0:
            self.health = 0

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

    return char('enemy', enemyTipe, randint(15*difMod, 20*difMod), randint(5*difMod, 7*difMod), randint(0+difMod, 3*difMod), specials)

def debugEnemy(enemy:char, allActions:dict, toughts:dict, action:str):
    print('ENEMY DEBUGGER !!!!!')
    for s in enemy.specials:
        print(f"{s} - {ALL_SPECIALS[s]['effect']}:{ALL_SPECIALS[s]['uses']}PP")
    print(f'all actions: {allActions}\ntoughts: {toughts}\naction: {action}')

def enemyAI(enemy:char, player:char):
    possibleActions = {'attack':1}
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
    elif choosenAction in ALL_SPECIALS.keys():
        enemy.use_special(choosenAction, player)
    
    #debugEnemy(enemy, possibleActions, thought, choosenAction)

def setWorldDif(playerLvl):
    dif = 'easy'

    if playerLvl == 1:
        dif = 'easy'
    elif playerLvl == 3:
        dif = 'medium'
    elif playerLvl == 5:
        dif = 'hard'
    elif playerLvl >= 7:
        dif = 'impossible'
    
    return dif

#----------------------------------------------------------------------------------#
#-------------------------------main program running-------------------------------#
#----------------------------------------------------------------------------------#

player = playerChar('Shy', 'fire', 100, 10, 2, {'sleep':2})
player.inv['health potion'] = 1

difficulty = setWorldDif(player.Level)
enemy = randomEnemy(difficulty)  



running = True
while running:
    while player.health and enemy.health > 0:

        print(f'{player.name} : {player.element} || {enemy.name} : {enemy.element}')
        print(f'health: {player.health} || health: {enemy.health} \n')

        player.updateStatus()

        while True:
            if player.canAct():
                moves = ['attack', 'special', 'items', 'info']
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
                            if choosenSpell in player.specials.keys() and player.specials[choosenSpell] > 0:
                                break
                            elif choosenSpell not in player.specials.keys():
                                print("You don't have that spell !!!")
                            else:
                                ('The spell has no PP left !!!')
                        player.use_special(choosenSpell, enemy)
                        okCheck()
                    case 'items':
                        print('inventory:')
                        for it, qntt in player.inv.items():
                            print(f'{it} * {qntt} -> ')
                        
                        choosenItem = input('choose an item or write "back": ')
                        if choosenItem in player.inv.keys():
                            player.useItemDef(choosenItem)
                            break
                        elif choosenItem == 'back':
                            continue
                        else:
                            print('invalid item!')
                    case 'info':
                        print(player.name)
                        print(f'element: {player.element} | Level: {player.Level}')
                        print(f'Current XP: {player.XP} | XP to next level: {player.XPnextLevel}')
                        print(f'health: {player.health}/{player.maxHealth}\ndamage: {player.dmg}\nresistance: {player.res}')
                        print('specials:')
                        for s in player.specials:
                            print(f'-{s} ->\n'
                                f"  effect: {ALL_SPECIALS[s]['effect']}\n"
                                f"  type: {ALL_SPECIALS[s]['type']}"
                                f"  PP: {ALL_SPECIALS[s]['uses']}\n")
                    case _:
                        if action in player.specials.keys(): 
                            if player.specials[action] > 0:
                                player.use_special(action, enemy)
                                okCheck()
                                break
                            else:
                                print('spell without PP !!!')
                                okCheck()
                        elif action in player.specials.keys() and action in ALL_SPECIALS.keys():
                            print('you dont have that spell!')
                            okCheck()
                        else:
                            print('invalid input !')
            else:
                break
        print('-----------')
        print(f'{player.name} : {player.element} || {enemy.name} : {enemy.element}')
        print(f'health: {player.health} || health: {enemy.health} \n')

        if enemy.health > 0 and enemy.canAct():
            print('ENEMY TURN !')
            enemyAI(enemy, player)
        elif enemy.health <= 0:
            print(f'{enemy.name} died!!!')

        if len(enemy.status) > 0 and enemy.health > 0:
                enemy.updateStatus()

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
                
                difficulty = setWorldDif(player.Level)
                enemy = randomEnemy(difficulty)

                system('cls' if name == 'nt' else 'clear')
                break
            case 'no' | 'n':
                running = False
                break
            case _:
                print('Unhandled answer, please tipe again !')
    