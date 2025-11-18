ITEMS_DICT = {'health potion':'heals 25 health'}

class item:

    def __init__(self, name:str):
        self.name = name

    def useItem(self, user):
        it_obj = item(self)

        if it_obj.name in user.inv.keys():
            print(f'{user.name} used {it_obj.name}!')

            match it_obj.name:
                case 'health potion':
                    user.health += 20
                    print('it healded 20 health!')
            
            user.inv[it_obj.name] -= 1
        elif it_obj.name in ITEMS_DICT.keys():
            print("you don't have that item !!!")
        else:
            print("this item doest't exist !!!")
        
        if user.inv[it_obj.name] <= 0:
            del user.inv[it_obj.name]