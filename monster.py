import random
import updater

class Monster:
    def __init__(self, name, health, room):
        self.name = name
        self.health = health
        self.room = room
        room.addMonster(self)
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
        if self.room.playerHere:
            return self.room
        for room in self.room.exits:
            if room[1].playerHere:
                return room[1]
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
    #Basic navigation
    def navigate(self,start,destination):
        i = 0
        path = []
        currRoom = start
        while (i < 100) and (currRoom != destination):
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

class Assignment(Monster):
    def __init__(self, name, health, room, damage, speed):
        super().__init__(name, health, room)
        self.damage = damage
        self.speed = speed
        self.cooldown = 0
        
    def update(self):
        if (random.randint(0,4) < 2) and (self.room.playerHere != True):
            path = self.player_path(self.room)
            #If there's more path than speed, move along the path up to my speed. Else, immediately move to 
            # the end of the path, without overshooting it.
            if self.speed <= len(path):
                self.moveTo(path[(self.speed - 1)])
            else:
                self.moveTo(path[(len(path) - 1)])

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

class Presentation(Assignment):
    monsterType = "Presentation"

class ProblemSet(Assignment):
    monsterType = "Problem Set"