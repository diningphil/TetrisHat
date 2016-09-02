# TetrisHat
Tetris with Raspberry Sense Hat LED matrix

## Notice
   In order to prevent the input thread from blocking on user input (thus allowing it to terminate) I have slightly modified the source code of python-sense-hat (you can find a fork of the repo in my profile) in order to allow a timeout to be set. The folder pythonsensehat contains the source with that change.
   I have opened a pull request, hopefully the owners will merge it into the master branch.

## TODO
1. Fix "push" recognition
2. Check rotation boundaries on the right side of the game matrix

