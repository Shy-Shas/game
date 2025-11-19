ITEMS_DICT = {
    'health potion': 'heals 25 health',
    'mega potion': 'heals 50 health',
    'elixir': 'restores health to max',
    'mana crystal': 'restores 10 PP to all specials',
    'poison vial': 'enemy receives poison status for 4 turns',
    'sleep powder': 'enemy sleeps for 3 turns',
    'fire bomb': 'deals 20 fire damage',
    'thorns seed': 'enemy takes 5 damage each time it attacks for 3 turns',
    'shield charm': 'reduces incoming damage by 5 for 3 turns'
    }


def useItem(user, item, target):

    if item in user.inv.keys():
        print(f'{user.name} used {item}!')

        match item:
            case 'health potion':
                user.health += 20
                user.correctHealth()
                print('it healded 20 health!')
            case 'mega potion':
                user.health += 50
                user.correctHealth()
                print('it healded 50 health!')
            case 'elixir':
                user.health = user.maxHealth
                print('it healded for all the health!')
            case 'mana cristal':
                print('recovered spells PP!')
                from spellsFunctions import SPECIALS

                for s in user.specials:
                    user.specials[s] += 10
                    if user.specials[s] > SPECIALS[s]['uses']:
                        user.specials[s] = SPECIALS[s]['uses']
            case 'poison vial':
                print(f'{target.name} got poisoned!')
                for i in range(4):
                    target.status.append('poison')
            case 'sleep powder':
                print(f'{target.name} falls asleep!')
                for i in range(3):
                    target.status.append('sleep')
            case 'fire bomb':
                damage = 40 if target.element == 'grass' else 20
                target.health -= damage
                target.correctHealth()

                print(f'it deals {damage} fire damage!')
            case 'thorns seed':
                print(f'{target.name} will be hurt when attacking!')
                for i in range(3):
                    target.status.append('thorns')
            case 'shield charm':
                print(f'{user.name} takes less damage!')
                for i in range(3):
                    user.status.append('shield')
        
        user.inv[item] -= 1
    elif item in ITEMS_DICT.keys():
        print("you don't have that item !!!")
    else:
        print("this item doest't exist !!!")
    
    if user.inv[item] <= 0:
        del user.inv[item]