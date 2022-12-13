from room import *
from player import Player
from item import *
from monster import *
import os
import updater
import ctypes
from worldGenerator import createRandWorld

player = Player()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Helper function that prints the player's current situation
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

#Search a list for an item, returning either true or false
def inList(list, search):
    contained = False
    for item in list:
        if item == search:
            contained = True
    return contained

#Search through all rooms for items, and check if thoughts are in their proper destinations. 
# If they are, return True. If even one is out of place, return false.
def checkVictory(rooms):
    victory = True
    for room in rooms:
        for item in room.items:
            if item.__class__.__name__ == "Thought":
                if item.destination != room.name.lower():
                    victory = False
    return victory

#Given a room name and the list of rooms, return a room object with that name.
def findRoomByName(name,roomList):
    if name == "player":
        foundRoom = player
    else:
        foundRoom = None
        for room in roomList:
            if room.name == name:
                foundRoom = room
    return foundRoom

#Recursive function to find the most efficient path from a starting room to a destination room. 
# In a top level call, prepath should be [].
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

#Helper function that takes a list of rooms given by navigate() and returns a series of 
# exit directions to take to reach the destination.
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

#Helper function that takes a prompt and its valid responses and asks for input until it gets a valid response.
def inputChecker(question,validResponses):
    enteredInput = input(question)
    while enteredInput not in validResponses:
        print("Please enter a valid input.")
        print()
        enteredInput = input(question)
    return enteredInput

#Loop until the player gives a valid answer to the saving and loading prompt
loading = inputChecker("Would you like to load a previous game? ",["yes","no"])

#This procedure loads the game from a series of saved text files.
if loading == "yes":

    #Helper function that constructs an item object from an item save file
    def load_item(filename,rooms):
        itemFile = open(filename, "r")
        itemName = itemFile.readline().replace("\n","")
        itemDesc = itemFile.readline().replace("\n","")
        itemRoomName = itemFile.readline().replace("\n","")
        itemWeight = int(itemFile.readline().replace("\n",""))
        itemLoc = findRoomByName(itemRoomName,rooms)
        currItem = Item(itemName,itemDesc,itemWeight,rooms)
        if itemLoc != player:
            currItem.putInRoom(itemLoc)
        else:
            player.pickup(currItem)

    #Helper function that constructs a monster function from a monster save file
    def load_monster(filename,rooms):
        monsterFile = open(filename, "r")
        monstName = monsterFile.readline().replace("\n","")
        monstHealth = int(monsterFile.readline().replace("\n",""))
        monsterRoomName = monsterFile.readline().replace("\n","")
        monsterRoom = findRoomByName(monsterRoomName,rooms)
        currMonster = Monster(monstName,monstHealth,monsterRoom,rooms)

    #Helper function that loads rooms and their exits from the ROOMS and WORLD files
    def load_world(savename):
        roomsName = savename + "_ROOMS.txt"
        filename = savename + "_WORLD.txt"

        #Open the file ROOMS and construct bare bones rooms with names only
        file = open(roomsName, "r")
        rooms = []
        line = file.readline().replace("\n","")
        while line != "":
            currRoom = Room("","")
            currRoom.name = str(line)
            rooms.append(currRoom)
            line = file.readline().replace("\n","")

        #Now that we have some rooms, fill them in with details like monsters and items
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
                    currRoom.addExit(exitList[0],exitList[1])
                    line = file.readline().replace("\n","")

            elif line == "START-FINAL-ATTRIBUTES":
                currRoom.desc = file.readline().replace("\n","")
                currRoom.playerHere = bool(file.readline().replace("\n",""))

            #If no conditions match, advance one line and repeat
            line = file.readline().replace("\n","")

        return rooms

    #Helper function that loads player attributes from a player save file
    def load_player(filename,rooms):
        file = open(filename, "r")
        location_name = file.readline().replace("\n","")
        player.location = findRoomByName(location_name,rooms)
        itemLine = file.readline().replace("\n","")
        if "ITEM.txt" in itemLine:
            load_item(itemLine,rooms)
        player.health = int(file.readline().replace("\n",""))
        player.alive = bool(file.readline().replace("\n",""))
        player.headspace = int(file.readline().replace("\n",""))
        player.name = file.readline().replace("\n","")
    
    #Simple loop to check if the entered save file is valid and request another one if it is not
    fileSuccess = False
    while not fileSuccess:    
        filecore = input("What save file would you like to load from? ")

        worldfile = filecore
        playerfile = filecore + "_PLAYER.txt"

        try:
            #Check if the player version of the file exists. If it does not, likely none of them will.
            open(playerfile, "r")
        except:
            print("No such save file.")
            print()
        else:
            rooms = load_world(worldfile)
            load_player(playerfile,rooms)
            fileSuccess = True
            print()
            print("Game loaded succesfully.")
            input("Press enter to continue...")
else:
    rooms = createRandWorld()
    player.location = rooms[0]
    rooms[0].playerHere = True

playing = True
possibleCommands = ["go","pickup","inventory","help","exit","attack","me","inspect","drop","wait","talk","save"]
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
        #Match input against possible commands based on mini slices of strings. Used to implement command abbreviations.
        for possibleCommand in possibleCommands:
            if possibleCommand[0:length] == slice:
                possibleMatches += 1
                match = possibleCommand
        #If there is a unique match to a command, autofill it. If not, proceed without doing anything.
        if possibleMatches == 1:
            commandWords[0] = match
        #Go to a new room
        if commandWords[0].lower() == "go":   #cannot handle multi-word directions
            player.goDirection(commandWords[1]) 
            timePasses = True
        #Wait for some (non-zero) time
        elif commandWords[0].lower() == "wait":   #Update the updater several iterations when asked
            #Helper function that triggers the updater a given number of times
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
        #Pickup an object in a room
        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                commandSuccess = False
        elif commandWords[0].lower() == "help!" or commandWords[0].lower() == "help":  #summon a random guard to your aid if you get lost
            print("A labyrinth guard comes running to your rescue!")
            input("Press enter to continue...")
            labyrinthGuards = []
            #Search all rooms looking for labyrinth guards and return a list of them
            for room in rooms:
                for monst in room.monsters:
                    if "Labyrinth Guard" in monst.name:
                        labyrinthGuards.append(monst)
            #Pick a random labyrinth guard and summon him or her to the player's location.
            chosenGuard = random.choice(labyrinthGuards)
            chosenGuard.moveTo(player.location)
            #If the chosen guard is the stabby guard, print a quick warning
            if chosenGuard.name == "Labyrinth Guard Who Stabs People Who Ask Tricky Questions":
                print("Unfortunately, it happens to be the Labyrinth Guard Who Stabs People Who Ask Tricky Questions.")
                print()
                input("Press enter to continue...")
            chosenGuard.interact(player)
        #Print the player's current inventory
        elif commandWords[0].lower() == "inventory":
            player.inventory()        
        #Exit the game
        elif commandWords[0].lower() == "exit":
            playing = False
        #Attack an assignment
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                commandSuccess = player.engageActivity(target)
                printSituation()
            else:
                print("No such monster.")
                commandSuccess = False
        #Talk to a creature capable of talking
        elif commandWords[0].lower() == "talk":
            targetName = command[5:]
            target = player.location.getMonsterByName(targetName)
            #The getMonsterByName() function will return False if there is no monster by that name to be found. If so, 
            # proceed without interacting and request another input.
            if target != False:
                #Only interact if the target creature is something that can talk.
                if "Labyrinth Guard" in target.name:
                    target.interact(player)
                else:
                    print("You can't talk to that.")
            else:
                print("No such creature.")
                commandSuccess = False
        #Print the player's current status.
        elif commandWords[0].lower() == "me":
            player.me()
        #Save the game
        elif commandWords[0].lower() == "save":

            #Save the attributes of a specific monster object to a unique text file, 
            # named with the monster's name plus a prefix and suffix
            def save_monster(savename,monster):
                filename = savename + "_" + monster.name + "_" + "MONSTER" + ".txt"
                file = open(filename, "w")
                file.write(str(monster.name) + "\n")
                file.write(str(monster.health) + "\n")
                file.write(str(monster.room.name) + "\n")
                file.close()
                return filename

            #Save the attributes of a given item object to a unique text file, 
            # named with the item's name plus a prefix and suffix.
            def save_item(savename,item):
                filename = savename + "_" + item.name + "_" + "ITEM" + ".txt"
                file = open(filename, "w")
                file.write(str(item.name) + "\n")
                file.write(str(item.desc) + "\n")
                file.write(str(item.loc.name) + "\n")
                file.write(str(item.weight) + "\n")
                file.close()
                return filename

            #Save the attributes of the player to a PLAYER save file
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
            
            #Save the attributes of the world to two text files, ROOMS, which contains only room names, 
            # and WORLD, which contains full room attributes
            def save_world(savename):
                filename = savename + "_" + "WORLD" + ".txt"
                file = open(filename, "w")
                file.write("START-ROOMS-LIST" + "\n")
                for room in rooms:
                    file.write("START-NEW-ROOM" + "\n")
                    file.write(str(room.name) + "\n")
                    print("writing start new room")

                    #If the room contains monsters, write out a series of monster save files and write the names of 
                    # those files as lines in this top level file. Else, write "no-monsters"
                    if len(room.monsters) > 0:
                        for monster in room.monsters:
                            file.write(str(save_monster(savename,monster)) + "\n")
                    else:
                        file.write("no-monsters" + "\n")
                    
                    file.write("START-EXITS" + "\n")
                    for baseExit in room.exits:
                        file.write(str(baseExit[0]) + "," + str(baseExit[1]) + "\n")
                    file.write("END-EXITS" + "\n")

                    #If the room contains items, write out a series of item save files and write the names of those 
                    # files as lines in this top level file. Else, write "no-items"
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
        #Inspect an item, but only if it exists
        elif commandWords[0].lower() == "inspect":
            targetName = command[8:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.inspect(target)
            else:
                print("No such item.")
                commandSuccess = False
        #Drop an item, but only if it's already in the inventory
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
else:
    print("See you next time...")