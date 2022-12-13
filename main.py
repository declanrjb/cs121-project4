from room import *
from player import Player
from item import *
from monster import *
import os
import updater
import ctypes
from worldGenerator import createRandWorld

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
    thought1 = Thought("Thought1",0)
    i.putInRoom(center_brain)
    thought1.putInRoom(useful_programming)
    player.location = center_brain
    center_brain.playerHere = True
    Bob = Assignment("Bob the monster", 20, excuses, 7, 1)
    print(Bob.player_path(Bob.room))
    input("Press enter to continue...")

    return rooms

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def printSituation():
    clear()
    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following creatures:")
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
                if item.destination != room.name.lower():
                    victory = False
    return victory

def findRoomByName(name,roomList):
    if name == "player":
        foundRoom = player
    else:
        foundRoom = None
        for room in roomList:
            if room.name == name:
                foundRoom = room
    return foundRoom

def navigate(start,destination,prepath):
    if start == destination:
        return [destination]
    else:
        path = prepath + [start]
        currRoom = start
        while currRoom != destination:
            shortestPath = None
            targetExit = None
            for exit in currRoom.exits:
                exitRoom = exit[1]
                if (exitRoom in path) != True:
                    testPath = navigate(exit[1],destination,path)
                    if (shortestPath == None) or (len(testPath) < len(shortestPath)):
                        shortestPath = testPath
                        targetExit = exit[1]
            if targetExit == None:
                targetExit = currRoom.exits[random.randint(0,(len(currRoom.exits)-1))][1]
            currRoom = targetExit
            path.append(currRoom)
    return path

def directions(path):
    i = 0
    pathLength = len(path)
    directions = []
    while i < (pathLength-1):
        currRoom = path[i]
        for checkExit in currRoom.exits:
            if checkExit[1] == path[i+1]:
                directions.append(checkExit[0])
        i += 1
    return directions





loading = input("Would you like to load a previous game? ")
if loading == "yes":
    filecore = input("What save file would you like to load from? ")

    def load_item(filename,rooms):
        itemFile = open(filename, "r")
        itemName = itemFile.readline().replace("\n","")
        itemDesc = itemFile.readline().replace("\n","")
        itemRoomName = itemFile.readline().replace("\n","")
        itemWeight = int(itemFile.readline().replace("\n",""))
        itemLoc = findRoomByName(itemRoomName,rooms)
        currItem = Item(itemName,itemDesc,itemWeight)
        if itemLoc != player:
            currItem.putInRoom(itemLoc)
        else:
            player.pickup(currItem)

    def load_monster(filename,rooms):
        monsterFile = open(filename, "r")
        monstName = monsterFile.readline().replace("\n","")
        monstHealth = int(monsterFile.readline().replace("\n",""))
        monsterRoomName = monsterFile.readline().replace("\n","")
        monsterRoom = findRoomByName(monsterRoomName,rooms)
        currMonster = Monster(monstName,monstHealth,monsterRoom)
        monsterRoom.addMonster(currMonster)

    def load_world(savename):
        roomsName = savename + "_ROOMS.txt"
        filename = savename + "_WORLD.txt"

        file = open(roomsName, "r")
        rooms = []
        line = file.readline().replace("\n","")
        while line != "":
            currRoom = Room("","")
            currRoom.name = str(line)
            rooms.append(currRoom)
            line = file.readline().replace("\n","")

        file = open(filename, "r")
        line = file.readline().replace("\n","")
        while line != "":
            if line == "START-NEW-ROOM":
                currRoomName = file.readline().replace("\n","")
                currRoom = findRoomByName(currRoomName,rooms)

            elif "MONSTER.txt" in line:
                load_monster(line,rooms)

            elif "ITEM.txt" in line:
                load_item(line,rooms)

            elif line == "START-EXITS":
                line = file.readline().replace("\n","")
                while line != "END-EXITS":
                    exitList = line.split(",")
                    print(exitList)
                    currRoom.addExit(exitList[0],exitList[1])
                    line = file.readline().replace("\n","")

            elif line == "START-FINAL-ATTRIBUTES":
                currRoom.desc = file.readline().replace("\n","")
                currRoom.playerHere = bool(file.readline().replace("\n",""))

            line = file.readline().replace("\n","")

        return rooms

    def load_player(filename,rooms):
        file = open(filename, "r")
        location_name = file.readline().replace("\n","")
        for room in rooms:
            if room.name == location_name:
                player.location = room
        itemLine = file.readline().replace("\n","")
        if "ITEM.txt" in itemLine:
            load_item(itemLine,rooms)
        player.health = int(file.readline().replace("\n",""))
        player.alive = bool(file.readline().replace("\n",""))
        player.headspace = int(file.readline().replace("\n",""))
        player.name = file.readline().replace("\n","")
    
    worldfile = filecore
    rooms = load_world(worldfile)

    playerfile = filecore + "_PLAYER.txt"
    load_player(playerfile,rooms)

    print()
    print("Game loaded succesfully.")
    input("Press enter to continue...")
else:
    rooms = createRandWorld()
    player.location = rooms[0]
    rooms[0].playerHere = True
playing = True
possibleCommands = ["go","pickup","inventory","help","exit","attack","me","inspect","drop","wait","talk"]
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
        elif commandWords[0].lower() == "wait":   #Update the updater several iterations when asked
            def wait_some_turns(turns):
                i = 0
                while i < turns:
                    updater.updateAll()
                    i += 1
            turns = int(command[5:])
            wait_some_turns(turns)
            print(str(turns) + " time goes by. Time passes strangely in this place.")
            print()
            input("Press enter to continue...")
        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                commandSuccess = False
        elif commandWords[0].lower() == "help!":  #summon a random guard to your aid if you get lost
            print("A labyrinth guard comes running to your rescue!")
            input("Press enter to continue...")
            labyrinthGuards = []
            for room in rooms:
                for monst in room.monsters:
                    if "Labyrinth Guard" in monst.name:
                        labyrinthGuards.append(monst)
            chosenGuard = random.choice(labyrinthGuards)
            chosenGuard.moveTo(player.location)
            chosenGuard.interact(player)
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
                commandSuccess = player.engageActivity(target)
                printSituation()
            else:
                print("No such monster.")
                commandSuccess = False
        elif commandWords[0].lower() == "talk":
            targetName = command[5:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                target.interact(player)
            else:
                print("No such monster.")
                commandSuccess = False
        elif commandWords[0].lower() == "me":
            player.me()
        elif commandWords[0].lower() == "save":

            def save_monster(savename,monster):
                filename = savename + "_" + monster.name + "_" + "MONSTER" + ".txt"
                file = open(filename, "w")
                file.write(str(monster.name) + "\n")
                file.write(str(monster.health) + "\n")
                file.write(str(monster.room.name) + "\n")
                file.close()
                return filename

            def save_item(savename,item):
                filename = savename + "_" + item.name + "_" + "ITEM" + ".txt"
                file = open(filename, "w")
                file.write(str(item.name) + "\n")
                file.write(str(item.desc) + "\n")
                file.write(str(item.loc.name) + "\n")
                file.write(str(item.weight) + "\n")
                file.close()
                return filename

            def save_player(savename):
                filename = savename + "_" + "PLAYER" + ".txt"
                file = open(filename, "w")
                file.write(str(player.location.name) + "\n")
                if len(player.items) > 0:
                    for k in player.items:
                        file.write(save_item(savename,k) + "\n")
                else:
                    file.write("no-items" + "\n")
                file.write(str(player.health) + "\n")
                file.write(str(player.alive) + "\n")
                file.write(str(player.headspace) + "\n")
                file.write(str(player.name) + "\n")
                file.close()
            
            def save_world(savename):
                filename = savename + "_" + "WORLD" + ".txt"
                file = open(filename, "w")
                file.write("START-ROOMS-LIST" + "\n")
                for room in rooms:
                    file.write("START-NEW-ROOM" + "\n")
                    file.write(str(room.name) + "\n")
                    print("writing start new room")

                    if len(room.monsters) > 0:
                        for monster in room.monsters:
                            file.write(str(save_monster(savename,monster)) + "\n")
                    else:
                        file.write("no-monsters" + "\n")
                    
                    file.write("START-EXITS" + "\n")
                    for baseExit in room.exits:
                        file.write(str(baseExit[0]) + "," + str(baseExit[1].name) + "\n")
                    file.write("END-EXITS" + "\n")

                    if len(room.items) > 0:
                        for item in room.items:
                            file.write(str(save_item(savename,item)) + "\n")
                    else:
                        file.write("no-items" + "\n")

                    file.write("START-FINAL-ATTRIBUTES" + "\n")
                    file.write(str(room.desc) + "\n")
                    file.write(str(room.playerHere) + "\n")
                file.close()

                roomFileName = savename + "_" + "ROOMS" + ".txt"
                file = open(roomFileName, "w")
                for room in rooms:
                    file.write(str(room.name) + "\n")
                file.close()
            
            savename = input("Saving game. Enter a file name: ")
            save_player(savename)
            save_world(savename)
            print()
            print("Game saved succesfully.")
            input("Press enter to continue...")
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
        if checkVictory(rooms):
            player.ending = "victory"
            playing = False

clear()
if player.ending == "timeout":
    print("Oh no!\nYou didn't finish the assignment by the deadline.")
elif player.ending == "burnout":
    print("Oh no!\nYou got too bogged down with assigments and burnt out.")
elif player.ending == "victory":
    print("Congratulations! You organized your thoughts, completed the final project on time, and passed CS 121!!")