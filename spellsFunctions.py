SPECIALS = {
    'fireball':{'effect':'10 damage + d10', 'type':'fire', 'uses':2},
    'firebolt':{'effect':'12 damage', 'type':'fire', 'uses':5},
    'lava ground':{'effect':'(if d20 >=15) enemy burns for 5 turns', 'type':'fire','uses':3},

    'grace':{'effect':'+3 health + d10', 'type':'grass', 'uses':5},
    'sleep':{'effect':"(if d20 >= 10) enemy sleeps for 2 turns", 'type':'grass', 'uses':2},
    'thorn rain':{'effect':"3*d6 for damage", 'type':'grass', 'uses':5}
    }

REACTIONS = {
            'fire':['grass', 'ice'],
            'grass':['rock']
            }

from random import randint
class dices:
    ALL_DICES = ['d6', 'd10', 'd20']

    def d6Roll():
        roll = randint(1, 6)
        print(f'd6 rolls a {roll}')
        return roll
    
    def d10Roll():
        roll = randint(1, 10)
        print(f'd10 rolls a {roll}')
        return roll
    
    def d20Roll():
        roll = randint(1, 20)
        print(f'd20 rolls a {roll}')
        return roll

def cew(targetElement:str, spellType): #Check Elemental Weakness
    if targetElement in REACTIONS[spellType]:
        return 2
    else:
        return 1

#spells-------------------
def fireball(target):
    roll = dices.d10Roll()
    damage = (10 + roll - target.res) * cew(target.element, 'fire')

    print(f'fireball does {damage} damage!')
    target.health -= damage

def firebolt(target):
    damage = (10 - target.res) * cew(target.element, 'fire')
    
    print(f'fireball does {damage} damage!')
    target.health -= damage

def lavaGround(caster:str, target):
    if dices.d20Roll() >= 15:
        for i in range(5):
            target.status.append('burn')
        
        print(f"a lava pool appears on {target.name}'s feet!")
        print(f'{target.name} is now burning!')
    else:
        print(f'{caster} missed the spell!!!')

def grace(target):
    healing = 3 + dices.d10Roll()
    print(f'{target.name} heals for {healing} health!')
    target.health += healing

def sleep(caster:str, target):
    if dices.d20Roll() >= 10:
        for i in range(3):
            target.status.append('sleep')
        print(f'{target.name} is now sleeping!')
    else:
        print(f'{caster} missed the spell')

def thornRain(target):
    damage = 0
    for i in range(3):
        damage += dices.d6Roll()
    
    target.health -= damage * cew(target.element, 'grass')
    print(f'thorns rain down upon {target.name}!')
    print(f'{target.name} takes {damage} damage!')