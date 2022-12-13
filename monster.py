import random
import updater

class Monster:
    def __init__(self, name, health, room, world):
        self.name = name
        self.health = health
        self.room = room
        room.addMonster(self)
        self.world = world
        updater.register(self)
    def update(self):
        if random.random() < .5:
            self.moveTo(self.room.randomNeighbor())
    def moveTo(self, room):
        self.room.removeMonster(self)
        self.room = room
        room.addMonster(self)
    def die(self):
        self.room.removeMonster(self)
        updater.deregister(self)
    def findPlayer(self):
        """Detects where the player is if the player is in the same
        or an adjacent room."""
        playerRoom = None
        if self.room.playerHere:
            playerRoom = self.room
        for room in self.room.exits:
            if room[1].playerHere:
                playerRoom = room[1]
        return playerRoom
    #Basic pathfinding
    def player_path(self,start):
        i = 0
        path = []
        currRoom = start
        while (i < 100) and (currRoom.playerHere != True):
            j = 0
            numExits = len(currRoom.exits)
            targetExit = currRoom.exits[j][1]
            while (targetExit in path) and (j < numExits):
                targetExit = currRoom.exits[j][1]
                j += 1
            currRoom = targetExit
            path.append(currRoom)
            i += 1
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
    
    def findRoomByName(self,name,roomList):
        foundRoom = None
        for room in roomList:
            if room.name == name:
                foundRoom = room
        return foundRoom

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
                        testPath = self.navigate(exit[1],destination,path)
                        if (shortestPath == None) or (len(testPath) < len(shortestPath)):
                            shortestPath = testPath
                            targetExit = exit[1]
                if targetExit == None:
                    targetExit = currRoom.exits[random.randint(0,(len(currRoom.exits)-1))][1]
                currRoom = targetExit
                path.append(currRoom)
        return path

class Assignment(Monster):
    def __init__(self, name, health, room, damage, speed, world, type):
        super().__init__(name, health, room, world)
        self.damage = damage
        self.speed = speed
        self.cooldown = 0
        self.world = world
        self.monsterType = type
        
    def update(self):
        i = 0
        while i < self.speed:
            if self.findPlayer() != None:
                self.moveTo(self.findPlayer())
            else:
                self.moveTo(random.choice(self.room.exits)[1])
            i += 1


class Leisure(Monster):
    monsterType = "Leisure"
    def __init__self(self, name, health, room, cost, buff):
        Monster.__init___(self, name, health, room)
        self.cost = cost #The time it takes to do the activity
        self.buff = buff #The amount of mental health healed

class Essay(Assignment):
    monsterType = "Essay"

class Test(Assignment):
    monsterType = "Test"

class Guard(Monster):
    def __init__(self,name,room,world):
        self.name = name
        self.health = 1
        self.room = room
        room.addMonster(self)
        self.world = world
        self.monsterType = "Test"
        updater.register(self)
    
    def update(self):
        #do nothing
        self.name = self.name
        
class HelpfulGuard(Guard):
    def __init__(self,name,room,world):
        Guard.__init__(self,name,room,world)
    
    def interact(self,player):
        openingMessage = "Well met stranger. What brings you to this place?"
        exitCondition = False
        while not exitCondition:
            print(openingMessage)
            print()
            print("[1] Where am I?")
            print("[2] What should I do?")
            print("[3] Ask for directions")
            print("[4] Ask for possible actions")
            print("[5] Leave")
            choice = input("")
            while not (1 <= int(choice) <= 5):
                print("Please choose a valid conversation starter.")
                choice = input("")
            choice = int(choice)
            if choice == 1:
                print("You are deep in the center of your own mind, brought here to conquer your anxieties and organize your thoughts in time to finish the final project for CSCI 121 at Reed College. To succeed, you must find the 10 thoughts scattered throughout your brain and return them to the chambers they are meant for. But beware, this place is more real than you know.")
                print()
                input("Press enter to continue...")
            elif choice == 2:
                print("You must find the 10 thoughts scattered throughout your brain and return them to the chambers they are meant for. Hurry! Time is running out.")
                print()
                input("Press enter to continue...")
            elif choice == 3:
                print("Where would you like to go?")
                destinationName = input("")
                destinationRoom = self.findRoomByName(destinationName,self.world)
                if destinationRoom != None:
                    print("Hmm, let me think...")
                    path = self.navigate(self.room,destinationRoom,[])
                    pathDirections = self.directions(path)
                    pathLength = len(pathDirections)
                    i = 0
                    message = ""
                    while i < pathLength:
                        if i == 0:
                            message += "Go "
                        else:
                            message += ", then "
                        message += pathDirections[i]
                        i += 1
                    print(message)
                else:
                    print("I'm sorry, I don't know where that is.")
                input("Press enter to continue...")
            elif choice == 4:
                print("Sure, you can:")
                print("go <direction> -- move you in the given direction")
                print("inventory -- open your inventory")
                print("pickup <item> -- pick up the item")
                print("help -- summon me or one of my colleagues")
                print("exit -- quit the game")
                print("attack <assignment> -- engage an assignment you are confronted with")
                print("me -- display your current status and inventory")
                print("inspect <item> -- inspect an item in your vicinity")
                print("drop <item> -- drop an item from your inventory")
                print("wait <turns> -- passes the given number of turns of time")
                print("talk <creature> -- engage someone in conversation")
                print()
                input("Press enter to continue...")
            elif choice == 5:
                return True
            openingMessage = "Anything else?"

class UnhelpfulGuard(Guard):
    def __init__(self,name,room,world):
        Guard.__init__(self,name,room,world)
    
    #Function to find the least efficient path from one room to another
    def navigate_badly(self,start,destination,prepath):
        if start == destination:
            return [destination]
        else:
            path = prepath + [start]
            currRoom = start
            while currRoom != destination:
                longestPath = None
                targetExit = None
                for exit in currRoom.exits:
                    exitRoom = exit[1]
                    if (exitRoom in path) != True:
                        testPath = self.navigate_badly(exit[1],destination,path)
                        if (longestPath == None) or (len(testPath) > len(longestPath)):
                            longestPath = testPath
                            targetExit = exit[1]
                if targetExit == None:
                    targetExit = currRoom.exits[random.randint(0,(len(currRoom.exits)-1))][1]
                currRoom = targetExit
                path.append(currRoom)
        return path

    def interact(self,player):
        openingMessage = "Well met stranger. What brings you to this place?"
        exitCondition = False
        while not exitCondition:
            print(openingMessage)
            print()
            print("[1] Where am I?")
            print("[2] What should I do?")
            print("[3] Ask for directions")
            print("[4] Leave")
            choice = input("")
            while not (1 <= int(choice) <= 4):
                print("Please choose a valid conversation starter.")
                choice = input("")
            choice = int(choice)
            if choice == 1:
                print("You are deep in the center of your own mind, brought here to conquer your anxieties and organize your thoughts in time to finish the final project for CSCI 121 at Reed College. To succeed, you must find the 10 thoughts scattered throughout your brain and return them to the chambers they are meant for. But beware, this place is more real than you know.")
                print()
                input("Press enter to continue...")
            elif choice == 2:
                print("You must find the 10 thoughts scattered throughout your brain and return them to the chambers they are meant for. Hurry! Time is running out.")
                print()
                input("Press enter to continue...")
            elif choice == 3:
                print("Where would you like to go?")
                destinationName = input("")
                destinationRoom = self.findRoomByName(destinationName,self.world)
                if destinationRoom != None:
                    print()
                    print("Hmm, let me think...")
                    print()
                    path = self.navigate_badly(self.room,destinationRoom,[])
                    pathDirections = self.directions(path)
                    pathLength = len(pathDirections)
                    i = 0
                    message = "I think the most efficient way would be to "
                    while i < pathLength:
                        if i == 0:
                            message += "go "
                        else:
                            message += ", then "
                        message += pathDirections[i]
                        i += 1
                    message += ". And you should definitely trust my advice."
                    print(message)
                else:
                    print("I'm sorry, I don't know where that is.")
                print()
                input("Press enter to continue...")
            elif choice == 4:
                return True
            openingMessage = "Anything else?"

class StabbyGuard(Guard):
    def __init__(self,name,room,world):
        Guard.__init__(self,name,room,world)
    
    def interact(self,player):
        if player.stabWounds == 0:
            print("'Stab!'")
            print()
            print("He stabs you. To be fair, you kind of should have seen this coming. Your physical and mental health both decrease by 1.")
        elif player.stabWounds < 2:
            print("'Stab!'")
            print()
            print("He stabs you again. To be fair, you kind of should have seen this coming. Your physical and mental health both decrease by 1.")
        else:
            print()
            print("He just looks at you with dissapointment. It's time for you to move on from this place.")
        player.health -= 1
        player.headspace -= 1
        player.stabWounds += 1
        print()
        input("Press enter to continue...")
