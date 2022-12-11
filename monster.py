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

    def path_to_player(self,player):
        path = []
        
    def update(self):
        if random.random() < self.speed:
            if self.findPlayer() in self.room.exits:
                self.moveTo(self.findPlayer())
            if self.findPlayer() == None:
                self.moveTo(self.room.randomNeighbor())

class Leisure(Monster):
    def __init__self(self, name, health, room, cost, buff):
        Monster.__init___(self, name, health, room)
        self.cost = cost #The time it takes to do the activity
        self.buff = buff #The amount of mental health healed