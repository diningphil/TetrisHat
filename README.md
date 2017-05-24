# TetrisHat
Tetris with Raspberry Sense Hat LED matrix

## TODO
1. Fix list assignment out of range errors which happen when I rotate near the right border  
2. Use callback mechanism provided by python sense hat library to handle the stick thread (adding a timeout parameter to the wait_for_event method is not a good idea, it does not consider some parts of the implementation
