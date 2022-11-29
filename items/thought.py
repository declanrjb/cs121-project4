from items.item import Item
import random

class Thought(Item):
    def __init__(self, name, destination):
        Item.__init__(self, name, "This is a thought.")
        self.destination = destination
        #Declare a preset list of possible blurbs
        blurbs = [
            "I really need to do the HUM reading",
            "Excuse me, but real programmers use butterflies",
            "Python is such a lovely language",
            "I love not having to type semicolons at the end of every line",
            "My computer is literally haunted",
            "I hope nobody checks the documentation for this bit",
            "This must be Thursday, I never could get the hang of Thursdays",
            "I love deadlines. I love the whooshing sound they make as they go by",
            "Omg, it was 42 all along",
            "Screw it, I'll just use a for loop",
            "Whoa",
            "Take off and nuke it from orbit - it's the only way to be sure"
        ]
        #Pick a blurb for this thought from the list at random
        self.blurb = blurbs[random.randint(0,(len(blurbs)-1))]
    
    def printBlurb(self):
        #Prints the blurb in italics using an ANSI escape sequence
        print("You think: " + "\x1B[3m" + self.blurb + "," + "\x1B[0m" + " and then shelve that for later.")
        print()
        input("Press enter to continue...")