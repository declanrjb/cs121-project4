import os
import updater
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = {}
        self.health = 50
        self.health_max = self.health
        self.alive = True
        self.headspace = 50
        self.headspace_max = self.headspace
        self.name = "player"
        self.timeLeft = 1000
        updater.register(self)
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

    #Function to find the shortest path from one room to another
    def navigate(self,start,destination,prepath):
        if start == destination:
            return [destination]
        else:
            path = prepath + [start]
            currRoom = start
            while currRoom != destination:
                shortestPath = None
                targetExit = None
                for exit in currRoom.exits:
                    exitRoom = exit[1]
                    if (exitRoom in path) != True:
                        print(exit[1].name)
                        print(destination.name)
                        testPath = self.navigate(exit[1],destination,path)
                        if (shortestPath == None) or (len(testPath) < len(shortestPath)):
                            shortestPath = testPath
                            targetExit = exit[1]
                if targetExit == None:
                    targetExit = currRoom.exits[random.randint(0,(len(currRoom.exits)-1))][1]
                currRoom = targetExit
                path.append(currRoom)
        return path

    #Helper function that translates paths from navigate into exit directions
    def directions(self,path):
        i = 0
        pathLength = len(path)
        directions = []
        while i < (pathLength-1):
            currRoom = path[i]
            for checkExit in currRoom.exits:
                if checkExit[1] == path[i+1]:
                    directions.append(checkExit[0])
            i += 1
        return directions

    def drop(self, item):
        #Remove all copies of the item
        while item in self.items.keys():
            self.items.pop(item)
            item.loc = self.location
            self.location.addItem(item)
            self.headspace += item.weight
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
        print("I have " + str(self.timeLeft) + " time left.")
        input("Press enter to continue...")
    def engageActivity(self, mon):
        clear()
        if mon.monsterType == "Leisure":
            print("You take " + str(mon.cost) + " time to " + mon.name + " and feel a bit better!")
            self.timeLeft -= mon.cost
            self.me()
        else:
            print("You decide to tackle " + mon.name + ".")
            print()
            if mon.monsterType == "Essay":
                self.time -= mon.health
                print("You spend " + str(mon.health) + " time working on " + mon.name +".")
            if mon.monsterType == "Test":
                self.health -= mon.health
                print("You take " + mon.name + ", it's stressful.")
            if random.random() > mon.health/self.health:
                print("You've successfully completed " + mon.name + "!")
                mon.die()
            else:
                print("Not done yet...")
        print()
        input("Press enter to continue...")

    def update(self):
        self.timeLeft -= 1
        if self.timeLeft <= 0:
            self.alive = False
            self.ending = "timeout"
        #Regeneration
        if self.health < self.health_max:
            self.health += 1
        #Assignments cause damage over time
        '''for assignment in self.location.monsters:
            if assignment.monsterType in ["Essay", "Test", "Presentation", "ProblemSet"]:
                self.health -= assignment.damage'''
        #When health reaches 0, you're forced to wait a random amount of time to heal.
        if self.health <= 0:
            print("#@*%")
            print("You're too stressed and need to relax.")
            for time in range(random.randint(0,50)):
                updater.updateAll
            #If you're too bogged down with assingments to heal, you lose.
            if self.health <= 0:
                self.alive = False
                self.ending = "burnout"
            self.me()