# minecraft_auto_fish
Minecraft Auto Fish


# Description:

This Python script automatically fishes for you on Mincecraft.  It does this by watching the bobber and when it sees the bobber disapper, it uses pyautogui to create a mouse click.  It then automatically re-casts the bobber.


# Installation:

* install latest version of python from https://www.python.org/downloads/

* checkout or clone this github project to a folder.
    * https://github.com/chiplukes/minecraft_auto_fish/archive/refs/heads/main.zip
    * git clone https://github.com/chiplukes/minecraft_auto_fish (if you have git installed)

* open a shell inside folder (cmd or windows terminal)

* run setup.bat
    * this creates a virtual environment in this folder and installs necessary packages (numpy, pyautogui, etc.)

* for conveniance, you can edit the autofish.bat file with the correct path for where you placed py_auto_fish on your pc. Then right click and make a shortcut and copy this to your desktop.

# Usage

First, you should find or create a nice safe place to fish if you plan on being AFK :)  I like to build a walled in area, with leaves on top of the walls so that mobs do not spawn on top

In theory you need at least a 5x5x2 pool of water, but I would go bigger so that you have some flexibility when you cast.  Otherwise you have to cast the bobber into the exact center block.

Build a platform that consists of a hopper and chest to catch any loot (preferably a chain of many hoppers and chests).  Just watch any of the pre 1.16 AFK fishing designs on youtube for examples.

Once you have the place to fish you can press ??? to run minecraft in a window.  You want some space next to this window to have the python program running with a bobber view window as well as the command prompt.  Also, it works best to have the autofish shortcut in this space on the desktop.

Cast bobber to spot you want to fish at.

Press ESC key.

Double click on autofish shortcut.

Follow instructions in command prompt.  In general you are moving the mouse pointer to where you want things and then pressing the enter key.  You need to do this with the cmd window active (don't click on mouse on any other windows)

* move mouse to upper lefthand corner of imaginary rectangle around bobber, then press enter.
* move mouse to lower righthand corner of imaginary rectangle around bobber, then press enter.
* move mouse to where you want to cast (crosshairs), then press enter.
* move mouse to where you want the bobber view window placed (somewhere next to minecraft window), then press enter.

Finally, you will be given 5 seconds to click the back to game button and cast the bobber (if it is not already cast).

After the 5 seconds you should see the red part of the bobber show up in the bobber view window.  This is a live view of what the python script is seeing.  Whenever the red goes away, it performs a mouse click.

# Why?

Short answer:

It is fun to solve problems using Python!

Longer answer:

This was built to help out on a Minecraft world that I play on with my son.  Fishing in Minecraft is a really simple way to get XP and obtain enchantments such as mending.  Starting in 1.16 Mojang removed the ability to easily fish for treasure.  We were curious to test how much treasure can be gathered by AFK fishing.

## License

[MIT](https://choosealicense.com/licenses/mit/)
