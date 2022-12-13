import os
import random
from monster import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, weight, world):
        self.name = name
        self.desc = desc
        self.loc = None
        self.weight = weight
        self.world = world
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

#A subclass of item that represents thoughts in the brain which have to be collected and organized. 
# Each has a "blurb", the thought itself, and a "destination" attribute that designates a room it must 
# be placed in in order for the victory condition to be achieved.
class Thought(Item):
    def __init__(self, name, weight, world):
        Item.__init__(self, name, "This is just a thought.", weight, world)
        #Declare a preset list of possible blurbs
        self.blurbs = {
            "I really need to do the HUM reading":"productive_thought",
            "Excuse me, but real programmers use butterflies":"programmer_humor",
            "Python is such a lovely language":"useful_programming",
            "I love not having to type semicolons at the end of every line":"useful_programming",
            "My computer is literally haunted":"programmer_humor",
            "I hope nobody checks the documentation for this bit":"lazy_hacks",
            "This must be Thursday, I never could get the hang of Thursdays":"sci_fi",
            "I love deadlines. I love the whooshing sound they make as they go by":"sci_fi",
            "Screw it, I'll just use a for loop":"lazy_hacks",
            "Whoa":"sci_fi",
            "Take off and nuke it from orbit - it's the only way to be sure":"sci_fi"
        }
    
    #Helper function that sets a blurb and destination based on a dictionary place index. Called by the world 
    # generator to ensure that each thought is unique.
    def pick_blurb(self,n):
        i = 0
        for key in self.blurbs:
            if i == n:
                self.blurb = key
            i += 1
        self.destination = self.blurbs[self.blurb]
    
    #Helper function that prints a thought in italic text
    def printBlurb(self):
        #Prints the blurb in italics using an ANSI escape sequence
        print("You think: " + "\x1B[3m" + self.blurb + "," + "\x1B[0m" + " and then shelve that for later.")
        print()
        input("Press enter to continue...")

    #Helper function that recalls the superclass's putInRoom while adding the additional behavior that a 
    # thought placed in excuses will spawn a new monster.
    def putInRoom(self, room):
        super().putInRoom(room)
        if room.name == "Room of Excuses":
            print("Unfortunately, by feeding excuses you have created more work for yourself. A new assignment materializes with a roar.")
            Assignment("HUM 110 Paper",random.randint(10,20),room,random.randint(10,20),random.randint(1,3),self.world)
            print()
            input("Press enter to continue...")
    
    #Simple version of put in room to be called by the world generator - preventing excuses spawn dialogue from playing 
    # while the world is building.
    def generatorPlace(self, room):
        super().putInRoom(room)