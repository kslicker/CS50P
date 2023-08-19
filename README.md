# Flappy Turd
#### Video Demo:  <https://youtu.be/3Z867teTUnc> 
## Description
Inspired by Flappy Bird, Flappy Turd is a game where you must keep a turd in the air and avoid pipes. The game is quite difficult as some pipes are very close together meaning they are almost impossible to pass. Each time you pass a bottom pipe you get a point. 

## How It Works
The Pygame library is used for graphics and animation. The background and pipes scroll by subtracting a defined amount from their X positions every cycle. The turd jumps everytime space key is pressed. Jump mechanics are controlled with velocity, gravity and jump height variables. If 'space key press' is detected velocity is equal to jump_height then the turd sprite Y position is decremented every cycle by velocity amount. Accordingly, velocity is decremented by gravity amount. 
The pipes coords are randomly generated and stored in a list. A minimum distance is checked so that the pipes aren't too close together. Their 'rects' are also stored in a list for collision detection purposes. The collision detection could be more accurate by using sprite collision detection but this requires an OOP approach and I decided to get this version done first. Pygame's 'collidelist' method is used to detect collision. This is called on the turd rect object and a list of pipe rects is passed to it. It is very simple to use except it only detects bounding rectangle collisions but the turd sprite is an irregular shape. This is where the collision inaccuracies are.
There is a also a Python test file which tests three of the functions in the game.

## Final Thoughts
Pygame is a fun library to use. I might do another version of this game but with an object oriented approach. I think this would reduce the amount of lines of code and allow me to do more precise collision detection.
 