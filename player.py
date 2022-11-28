import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.alive = True
    def goDirection(self, direction):
        self.location.playerHere = False
        self.location = self.location.getDestination(direction)
        self.location.playerHere = True
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.removeItem(item)
    def drop(self, item):
        while self.items.count(item) != 0:
            self.items.remove(item)
            item.loc = self
            self.location.addItem(item)
    def showInventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        print(self.items)
        input("Press enter to continue...")
    def inspect(self, item):
        print("You inspect the " + str(item.name) + ".")
        print(str(item.desc))
        print()
        input("Press enter to continue...")
    def me(self):
        clear()
        print("Checking self actualization", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".")
        time.sleep(1)
        print("You are currently in " + str(self.location.name))
        print("Your health is " + str(self.health))
        print("You are carrying: ")
        for i in self.items:
            print(i.name)
        print()
        if self.alive:
            print("And you aren't dead yet!")
        else:
            print("And you are now dead :(")
        input("Press enter to continue...")
    def attackMonster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")

