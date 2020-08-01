# jetbrains project
# coffee machine odering

import sys, operator

class CoffeeMachine:
    items = ["water", "milk", "beans", "cups"]
    items_dict = {'espresso': ((250, 0, 16, 1), 4), 
                  'latte': ((350, 75, 20, 1), 7), 
                  'cappuccino': ((200, 100, 12, 1), 6)
                 }    
    
    def __init__(self, water, milk, beans, cups, money):
        # starting qty of items
        self.qty = [water, milk, beans, cups]
        self.money = money
    
    def main(self):
        self.action_choice() 
        
    def print_state(self):
        print("The coffee machine has:")
        print(f"{self.qty[0]} ml of water")
        print(f"{self.qty[1]} ml of milk")
        print(f"{self.qty[2]} g of coffee beans")
        print(f"{self.qty[3]} disposable cups")
        print(f"${self.money} of money")
        print("")

    def action_choice(self):
        choice = input("Write action (buy, fill, take, remaining, exit):\n").strip().lower()
        print("")
        if choice == "buy":
            self.action_buy()
        elif choice == "fill":
            self.action_fill()
        elif choice == "take":
            self.action_take()
        elif choice == "remaining":
            self.action_remaining()
        elif choice == "exit":
            self.action_exit()    
        print("")
    
    def qty_decrease(self, option):
        # https://stackoverflow.com/a/534914/13944490
        # subtract required items from qty using map, convert back to list
        return list(map(operator.sub, self.qty, CoffeeMachine.items_dict[option][0]))
    
    def qty_check(self, option):
        check = self.qty_decrease(option)
        not_enough = False
        for i, qty in enumerate(check):
            if qty < 0:
                print(f"Sorry, not enough {self.items[i]}!")
                not_enough = True
        if not_enough:
            print("")
            return self.action_choice()
        else:
            return True           
    
    def translate_option(self, option):
        # unpack coffee options as a list, to translate numeric to key word
        # https://stackoverflow.com/a/45253740/13944490
        options = [*CoffeeMachine.items_dict.keys()]
        return options[option - 1]
    
    def action_buy(self):
        buy = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\nType 'back' to return to menu\n").strip()
        if buy == "back":
            self.action_choice()
        elif not 1 <= int(buy) <= 3:
            print("Choose a valid option please")
            return self.action_buy() 
        else:
            buy = self.translate_option(int(buy))
            self.qty_check(buy)
            self.qty = self.qty_decrease(buy)
            self.money += CoffeeMachine.items_dict[buy][1]
            print("I have enough resources, making you a coffee!")
            print("")
            return self.action_choice()
            
    def action_fill(self):
        self.qty[0] += int(input("Write how many ml of water do you want to add:\n"))
        self.qty[1] += int(input("Write how many ml of milk do you want to add:\n"))
        self.qty[2] += int(input("Write how many grams of coffee beans do you want to add:\n"))
        self.qty[3] += int(input("Write how many disposable cups of coffee do you want to add:\n"))
        print("")
        return self.action_choice()
        
    def action_take(self):
        if self.money > 0:
            print(f"I gave you ${self.money}")
            self.money -= self.money
        else:
            print("No money to take!")
        print("")
        return self.action_choice()
    
    def action_remaining(self):
        self.print_state()
        return self.action_choice()
        
    def action_exit(self):
        sys.exit()
        
coffeemachine = CoffeeMachine(400, 540, 120, 9, 550)
coffeemachine.main()     