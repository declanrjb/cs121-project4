from monsters.monster import Monster

class Leisure(Monster):
    def __init__self(self, name, health, room, cost, buff):
        Monster.__init___(self, name, health, room)
        self.cost = cost #The time it takes to do the activity
        self.buff = buff #The amount of mental health healed