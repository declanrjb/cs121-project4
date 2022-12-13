# cs121-project4
Total Points: 50+

(x) “me” command (2 points): Create a command that lets the player see their current status, including their health and/or whatever other attributes you’ve added.
    Added the "me" command which tells the player where they are, gives a short description based on how healthy they are, a readout of their inventory, and how much time they have left; can be found in player.
(x) bigger world (2 points): The game starts with four rooms. That is not enough for much to happen in. Make the world bigger and more interesting. Give descriptions to rooms that say more than just a room number.
    Added special "key rooms" which are crucial to the game; can be found in worldGenerator.
(x) “inspect” command (2 points): Create a command that lets the player look at items. This should display the item description. The player should be able to look at both items they see in their current location and items in their inventory.
    Items can be inspected, giving a readout of their description; can be found in player.
(x) limited inventory (2 points): Make objects you’re carrying have a size or weight, and put a limit on how much you can carry.
    The player has a limited "headspace", only being able to carry a few thoughts at a time; can be found in player.
(x) “drop” command (2 points): Make it so that the player can drop items, so that their inventory doesn’t become unreasonably large.
    The player can drop items from their inventory into the room they're in; can be found in player.
(x) item stacking (2 points): Make the inventory display ‘(x2)’ if there are two identical items (and so on, if there are more), rather than listing the item name twice.
    In the inventory display, items "stack"; can be found in player.
(x) introducing monsters during play (2 points): Make it so that over time new monsters appear in the world.
    When the player places "excuses", a big monster spawns; can be found in item.
(x) “wait” command (2 points): In the game as it is, time passes only when you move to a new room. Make it so that you can type a command that just lets time pass. Or implement a trickier version: let the user type a number so they can wait for a number of turns with only one command entry.
    The player can wait an amount of time that they specify; can be found in main.
(x) regeneration (2 points): Have the player regenerate in some way over time. The easiest thing is to make health increase a little each turn, but there are other things you could do as well.
    The player naturally regenerates 1 health each turn; can be found in player.
(x) victory condition (3 points): Create a way for the player to win the game.
    The player wins when they put all of the thoughts in their places; can be found in main and item.
(x) more monsters (3 points): Create several different types of monsters. They should not just have different names, but really be different in important ways.
    There are two types of monsters which drain different resources when you attack them, "Essays" drain your time and "Tests" drain your health; can be found in monster and player.
(x) command abbreviations (3 points): The typing needed to play a text adventure can get tedious. Usually games allow abbreviations. This could simply just be some short, alternate commands (“inv” instead of “inventory”, etc.) or, more ambitiously, you could accept any string that is the start of only one command. And/or you could allow items, monsters, and other things to be abbreviated in some consistent way.
    Commands can be autofilled from any abbreviation that matches a unique command; can be found in player
(x) characters (4 points): Characters are neutral beings in the game that you can talk to and interact with. (The “talking to” can be a matter of picking one of several options of things to say from a list.) They should interact with you or the world in some way when you talk to them. This should be different than the “helper” above (that is, if you make a helper character, then you need another character to get credit for this option).
    There are three labyrinth guards that can be talked to and asked for directions, background, or possible actions. They can also be summoned with the help command.
(x) navigation (6 points)
    Declan wrote a recursive function which finds the most efficient path from one room to another, and a second function that gives directions based on these "paths". The function is slow to run but very helpful for navigating the large procedural map.
(x) saving the game (10 points) : Let a player choose to save their game to come back to later. This should create a file in the folder where the program is stored (or maybe in a “saved” subfolder of that folder) with a name specified by the user. On starting the program, the user should have the option to continue from the point at which they saved, instead of creating a new game.
    The gamestate can be saved to a file which can be later loaded; can be found in main.
(x) random world (3+ points): Make the world be generated in a random way when the program is run so that it’s somewhat different each time the game is played.
    The world is somewhat randomly generated by creating randomly branching paths off of a central room, and then randomly connecting in key rooms, adding some extra connections between rooms, and spawning items and monsters; can be found in worldGenerator.

Work Division:
    Conceptualization for the game was done together in a brainstorm.
    From that point on we largely worked separately on different parts of the code at any given time, checking in frequently to maintain cohesion.
    Smaller elements (such as items, the "me" command, player regeneration, etcetera) went through several passes with both of us adding features to and refining them, often "passing them back and forth".
    Larger elements (such as the save system and the world generator) were each primarily worked on by one of us, with bug testing being collaborative.
    We coordinated our efforts using git (repository availabe at https://github.com/declanrjb/cs121-project4). 
    Declan worked on navigation, the saving and loading system, the victory condition, the wait command, the inspect command, 
    the drop command, command abbreviations, the labyrinth guards, the me command, introducing monsters during play, and regeneration