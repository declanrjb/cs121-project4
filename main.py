from room import *
from player import Player
from item import *
from monster import *
import os
import updater

player = Player()

def createWorld():
    #Build rooms
    center_brain = Room("center_brain","You are now in the center of the brain.")
    useful_programming = Room("useful_programming","You are now in the chamber of useful programming knowledge, a hallowed space filled mostly with CSC1 121 lecture notes.")
    lazy_hacks = Room("lazy_hacks","You are now in the room of lazy hacks. Every surface, from floor to walls to ceiling, is a chalkboard - but most of the notes you've taken there are covered up by the shelves of Stack Overflow comments.")
    programmer_humor = Room("programmer_humor","You have entered the sanctum of programmer humor, a place of many memes stolen from many subreddits.")
    bad_jokes = Room("bad_jokes","You are now in the room of bad jokes. And I mean *really* bad jokes. Abandon hope, all ye who enter here.")
    sci_fi = Room("sci_fi","You are now in the vault of out of place sci-fi references, a room strangely larger than any other in this brain.")
    productive_thought = Room("productive_thought","You are now in the room of productive academic thought. Sadly, there's quite a lot of dust here.")
    distractions = Room("distractions","You are now in the room of distractions - Hey, did you know the new NK Jemisin book just came out?")
    excuses = Room("excuses","Listen, it's not your fault you've entered the room of excuses. Somebody else made you do it.")

    rooms = [center_brain,useful_programming,lazy_hacks,programmer_humor,bad_jokes,sci_fi,productive_thought,distractions,excuses]

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

    i = Item("Rock", "This is just a rock.", 1)
    thought1 = Thought("Thought1",0,center_brain)
    i.putInRoom(center_brain)
    thought1.putInRoom(useful_programming)
    player.location = center_brain
    Assignment("Bob the monster", 20, excuses, 7, 1)

    return rooms

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

def checkVictory(rooms):
    victory = True
    for room in rooms:
        for item in room.items:
            if item.__class__.__name__ == "Thought":
                if item.destination != room:
                    victory = False
    return victory




rooms = createWorld()
playing = True
possibleCommands = ["go","pickup","inventory","help","exit","attack","me","inspect","drop"]
while playing and player.alive:
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()
        slice = commandWords[0].lower()
        length = len(slice)
        possibleMatches = 0
        match = ""
        for possibleCommand in possibleCommands:
            if possibleCommand[0:length] == slice:
                possibleMatches += 1
                match = possibleCommand
        if possibleMatches == 1:
            commandWords[0] = match
        if commandWords[0].lower() == "go":   #cannot handle multi-word directions
            player.goDirection(commandWords[1]) 
            timePasses = True
        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                commandSuccess = False
        elif commandWords[0].lower() == "inventory":
            player.inventory()        
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
            dropped = None
            itemsTemp = player.items
            for item in itemsTemp:
                if item.name.lower() == targetName.lower():
                    dropped = item
            if dropped != None:
                player.drop(dropped)
            else:
                print("You are not carrying that item.")
                commandSuccess = False
        elif commandWords[0].lower() == "checkvictory":
            print(str(checkVictory(rooms)))
            print()
            input("Press enter to continue...")
        else:
            print("Not a valid command")
            commandSuccess = False
    if timePasses == True:
        updater.updateAll()

    


