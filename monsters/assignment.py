from monsters.monster import Monster
import random

class Assignment(Monster):
    def __init__(self, name, health, room, damage, speed):
        super().__init__(name, health, room)
        self.damage = damage
        self.speed = speed
    def update(self):
        if random.random() < self.speed:
            if self.findPlayer() in self.room.exits:
                self.moveTo(self.findPlayer())
            if self.findPlayer() == None:
                self.moveTo(self.room.randomNeighbor())