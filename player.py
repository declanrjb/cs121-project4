import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = {}
        self.health = 50
        self.alive = True
        self.headspace = 50
        self.name = "player"
    def goDirection(self, direction):
        self.location.playerHere = False
        self.location = self.location.getDestination(direction)
        self.location.playerHere = True
    def pickup(self, item):
        if self.headspace - item.weight > 0:
            if item not in self.items.keys():    
                self.items[item] = 1
            else:
                self.items[item] += 1
            item.loc = self
            self.location.removeItem(item)
            self.headspace -= item.weight
            if item.__class__.__name__ == "Thought":
                item.printBlurb()
        else:
            print("Too many thoughts...\n...I need to clear my head a bit.")
    def drop(self, item):
        #Remove all copies of the item
        while item in self.items.keys():
            self.items.pop(item)
            item.loc = self.location
            self.location.addItem(item)
    def load(self,filename,rooms):
        file = open(filename, "r")
        location_name = file.readline().replace("\n","")
        print(location_name)
        for room in rooms:
            print(room)
            if room.name == location_name:
                self.location = room
        self.items = file.readline().replace("\n","")
        self.health = file.readline().replace("\n","")
        self.alive = file.readline().replace("\n","")
        self.headspace = file.readline().replace("\n","")
    def inventory(self):
        clear()
        print("I'm thinking about:")
        print()
        for item in self.items:
            print(item.name+"*"+str(self.items[item]))
        print()
        input("Press enter to continue...")
    def inspect(self, item):
        print("What's this? It seems to be a " + str(item.name) + ".")
        print(str(item.desc))
        print()
        input("Press enter to continue...")
    def me(self):
        clear()
        print("Checking self actualization...")
        print("I'm currently in " + str(self.location.name) + ",")
        if self.health < 10:
            print("AAaaaaaaaAAAAAAAAAaAaAaAaAaAAaAaAAaAaAaaaaaaAAaAAAaaAAaAaaaaAAAAAAA!")
        elif self.health < 20:
            print("and I could really use some chocolate right about now....")
        elif self.health < 30:
            print("and I exist.")
        elif self.health < 40:
            print("and every little thing gonna be alright.")
        else:
            print("and nothing can stop me!")
        print("I'm thinking about: ")
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

