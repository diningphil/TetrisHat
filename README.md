# TetrisHat
Tetris with Raspberry Sense Hat LED matrix

## Notice
   In order to prevent the input thread from blocking on user input (thus allowing it to terminate) I have slightly modified the source code of python-sense-hat (you can find a fork of the repo in my profile) in order to allow a timeout to be set. The folder pythonsensehat contains the source with that change.
   
## TODO
1. Fix "push" recognition
2. Implement canRotate which checks rotation boundaries on the right side of the game matrix ( rotation is always clockwise )
3. Use callback mechanism provided by python sense hat library to handle the stick thread (adding a timeout parameter to the wait_for_event method is not a good idea, it does not consider some parts of the implementation
