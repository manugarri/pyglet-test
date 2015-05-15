# pyglet-test
Attempt to make a dungeon rpg by reading the least amount of documentation. What could possibly go wrong?

###Why?

For three reasons:

1. The embarrasing lack of proper documentation for [pyglet](http://www.pyglet.org/documentation.html)
2. Because trying on my own might find good solutions that wouldn't exist otherwise if followed best practices since day 0
3. Because 2 will probably wont happen, but trying will make me learn more about game development than following a tutorial.

Because of `2.` I wouldn't recommend anybody using this repo as an example.

###Basics

Very basic game. With basic rule:

1. You are the good team. You win each level by defeating all of the bad guys.
2. You control a variable number of avatars:
  * *The Peasant* who is weak.
  * *The Knight* who is relatively strong in close combat.
  * and many more! (not implemented yet and probably will never be).
3. If all of your avatars die, the game restarts.

###Controls:

* <kbd>w</kbd> Move up
* <kbd>s</kbd> Move down
* <kbd>a</kbd> Move left
* <kbd>f</kbd> Move right
* <kbd>a</kbd> Attack
* <kbd>Space</kbd> Alternate avatars
* <kbd>Enter</kbd> End Turn
