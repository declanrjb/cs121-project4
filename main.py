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
    a = Room("You are in room 1")
    b = Room("You are in room 2")
    c = Room("You are in room 3")
    d = Room("You are in room 4")
    Room.connectRooms(a, "east", b, "west")
    Room.connectRooms(c, "east", d, "west")
    Room.connectRooms(a, "north", c, "south")
    Room.connectRooms(b, "north", d, "south")
    i = Item("Rock", "This is just a rock.")
    thought1 = Thought("Thought1",1)
    i.putInRoom(b)
    thought1.putInRoom(b)
    player.location = a
    Assignment("Bob the monster", 20, b, 7, 1)

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

    


