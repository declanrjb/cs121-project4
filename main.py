from rooms.room import Room
from player import Player
from items.item import *
from items.thought import *
from monsters.monster import Monster
from monsters.assignment import Assignment
import os
import updater

player = Player()

def createWorld():
    #Build rooms
    center_brain = Room("You are now in the center of the brain.")
    useful_programming = Room("You are now in the chamber of useful programming knowledge, a hallowed space filled mostly with CSC1 121 lecture notes.")
    lazy_hacks = Room("You are now in the room of lazy hacks. Every surface, from floor to walls to ceiling, is a chalkboard - but most of the notes you've taken there are covered up by the shelves of Stack Overflow comments.")
    programmer_humor = Room("You have entered the sanctum of programmer humor, a place of many memes stolen from many subreddits.")
    bad_jokes = Room("You are now in the room of bad jokes. And I mean *really* bad jokes. Abandon hope, all ye who enter here.")
    sci_fi = Room("You are now in the vault of out of place sci-fi references, a room strangely larger than any other in this brain.")
    productive_thought = Room("You are now in the room of productive academic thought. Sadly, there's quite a lot of dust here.")
    distractions = Room("You are now in the room of distractions - Hey, did you know the new NK Jemisin book just came out?")
    excuses = Room("Listen, it's not your fault you've entered the room of excuses. Somebody else made you do it.")

    #Build center_brain connections
    Room.connectRooms(center_brain,"north",useful_programming,"south")
    Room.connectRooms(center_brain,"east",productive_thought,"west")
    Room.connectRooms(center_brain,"south",distractions,"north")
    Room.connectRooms(center_brain,"west",sci_fi,"east")

    #Build useful_programming connections
    Room.connectRooms(useful_programming,"east",lazy_hacks,"west")
    Room.connectRooms(useful_programming,"west",programmer_humor,"east")

    #Build programmer_humor connections
    Room.connectRooms(programmer_humor,"west",bad_jokes,"east")
    Room.connectRooms(programmer_humor,"south",sci_fi,"north")

    #Build distractions connections
    Room.connectRooms(distractions,"south",excuses,"north")

    i = Item("Rock", "This is just a rock.")
    thought1 = Thought("Thought1",center_brain)
    i.putInRoom(center_brain)
    thought1.putInRoom(useful_programming)
    player.location = center_brain
    Assignment("Bob the monster", 20, excuses, 7, 1)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    clear()
    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for e in player.location.exitNames():
        print(e)
    print()

def showHelp():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print()
    input("Press enter to continue...")

#Search a list for an item, returning either true or false
def inList(list, search):
    contained = False
    for item in list:
        if item == search:
            contained = True
    return contained



createWorld()
playing = True
while playing and player.alive:
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        if commandWords[0].lower() == "go":   #cannot handle multi-word directions
            player.goDirection(commandWords[1]) 
            timePasses = True
        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "inventory":
            player.showInventory()        
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "exit":
            playing = False
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                player.attackMonster(target)
            else:
                print("No such monster.")
                commandSuccess = False
        elif commandWords[0].lower() == "me":
            player.me()
        elif commandWords[0].lower() == "inspect":
            targetName = command[8:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.inspect(target)
            else:
                print("No such item.")
                commandSuccess = False
        elif commandWords[0].lower() == "drop":
            targetName = command[5:]
            dropped = False
            for item in player.items:
                if item.name.lower() == targetName.lower():
                    player.drop(target)
                    dropped = True
            if dropped != True:
                print("You are not carrying that item.")
                commandSuccess = False
        else:
            print("Not a valid command")
            commandSuccess = False
    if timePasses == True:
        updater.updateAll()

    


