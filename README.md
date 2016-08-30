# TetrisHat
Tetris with Raspberry Sense Hat LED matrix

## Notice
   In order to prevent the input thread from blocking on user input (thus allowing it to terminate) I have slightly modified the source code of python-sense-hat in order to allow a timeout to be set. The folder pythonsensehat contains that change.
   I have opened a pull request, hopefully the owners will merge it into the master branch.

## TODO
0. Fix clearRows(). Other cells may fall down after a row has been deleted
2. Add rotation capabilities
3. Extend to different pieces at different starting positions
