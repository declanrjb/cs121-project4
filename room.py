import random

class Room:
    def __init__(self, name, description):
        self.desc = description
        self.monsters = []
        self.exits = []
        self.items = []
        self.name = name
        self.playerHere = False
    def addExit(self, exitName, destination):
        self.exits.append([exitName, destination])
    #Given an exit direction, return the room object that exit connects to
    def getDestination(self, direction):
        for e in self.exits:
            if e[0] == direction:
                print(e[1])
                return e[1]
    def connectRooms(room1, dir1, room2, dir2):
        #creates "dir1" exit from room1 to room2 and vice versa
        room1.addExit(dir1, room2)
        room2.addExit(dir2, room1)
    def exitNames(self):
        return [x[0] for x in self.exits]
    def addItem(self, item):
        self.items.append(item)
    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            return False
    def addMonster(self, monster):
        self.monsters.append(monster)
    def removeMonster(self, monster):
        self.monsters.remove(monster)
    def hasItems(self):
        return self.items != []
    def getItemByName(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def hasMonsters(self):
        return self.monsters != []
    def getMonsterByName(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
        return False
    def randomNeighbor(self):
        return random.choice(self.exits)[1]