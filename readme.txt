CS1830 Group 01 Project 'This Game Has Bugs (Galaxy Raiders)'
Project by: Callum Clapton, Lauren Moore, Oliver Fletcher and Sarah Wolstencroft

PROJECT STRUCTURE:
 - myGame.py is the main game file. It requires vector.py to run.
 - vector.py is the vector handling file.
 - menu.py is the standalone menu file, including menu sounds.
 - driver.py is the game-menu merge file, where we attempted to merge the menu code with our main game file. This was not
	successful, as explained below.

HOW TO RUN:
The file myGame.py will run outside of an IDE as long as you have the following packages.
 - PYTHON (Version 3)
 - PYGAME
 - SimpleGUICS2Pygame
 
The game is confirmed to work on Pygame version 1.9.4, SimpleGUICS2Pygame version 1.9.0 and Python version 3.7, but may work
with earlier or later versions of these pacakges.

As long as the myGame.py and vector.py file are located in the same directory, and the packages are installed correctly, the game will 
run normally. As 'super' is used within our game file, the code will not run through Codeskulptor 3 as it does not currently have 
support for this Python feature.

ISSUES WITH THE MENU:
We were unable to correctly merge our menu with our main game file. For the most part, running the driver.py file will load up our 
current menu, with control over moving up and down, selecting options and changing settings. Selecting the "Start Game" option will 
load up a version of the game, but a number of features are unusable, most notably player movement.

A standalone menu file is also included, so that the differences between the game and menu can still be seen.  Please note,
due to the way SimpleGUI handles sound, this file will ONLY work in CodeSkulptor 3.
