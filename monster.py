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

class Assignment(Monster):
    def __init__(self, name, health, room, damage, speed):
        super().__init__(name, health, room)
        self.damage = damage
        self.speed = speed
        self.cooldown = 0

    def path_to_player(self,currRoom):
        if currRoom.playerHere or len(currRoom.exits) == 0:
            return []
        else:
            numExits = len(currRoom.exits)
            '''
            shortestPath = None
            for exit in currRoom.exits:
                if exit[1]
                localPath = self.path_to_player(exit[1])
                if shortestPath == None or len(localPath) < len(shortestPath):
                    shortestPath = localPath
            '''
            targetExit = random.randint(1,numExits) - 1
            nextRoom = currRoom.exits[numExits-1][1]
            priorPath = self.path_to_player(nextRoom)
            return priorPath + [currRoom.name]

    #Basic pathfinding
    def player_path(self,currRoom):
        i = 0
        path = []
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
        
    def update(self):
        if (random.randint(0,4) < 2) and (self.room.playerHere != True):
            path = self.player_path(self.room)
            print(path)
            self.moveTo(path[0])

class Leisure(Monster):
    def __init__self(self, name, health, room, cost, buff):
        Monster.__init___(self, name, health, room)
        self.cost = cost #The time it takes to do the activity
        self.buff = buff #The amount of mental health healed