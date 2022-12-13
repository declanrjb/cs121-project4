import os
import random
from monster import *

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, weight):
        self.name = name
        self.desc = desc
        self.loc = None
        self.weight = weight
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def putInRoom(self, room):
        self.loc = room
        room.addItem(self)

class Thought(Item):
    def __init__(self, name, weight):
        Item.__init__(self, name, "This is just a thought.", weight)
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
        
    def pick_blurb(self,n):
        i = 0
        for key in self.blurbs:
            if i == n:
                self.blurb = key
            i += 1
        self.destination = self.blurbs[self.blurb]
    
    def printBlurb(self):
        #Prints the blurb in italics using an ANSI escape sequence
        print("You think: " + "\x1B[3m" + self.blurb + "," + "\x1B[0m" + " and then shelve that for later.")
        print()
        input("Press enter to continue...")

    def putInRoom(self, room):
        super().putInRoom(room)
        if room.name == "excuses":
            print("Unfortunately, by feeding excuses you have created more work for yourself. A new assignment materializes with a roar.")
            Assignment("HUM 110 Paper",random.randint(10,20),room,random.randint(10,20),random.randint(1,3))
            print()
            input("Press enter to continue...")