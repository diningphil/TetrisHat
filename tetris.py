from sense_hat import SenseHat
import thread
import time
import signal
import sys

sense = SenseHat()
#sense.set_rotation(180)

def sig_handler(signal, frame):
    sense.clear()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

X = [255, 0, 0]  # Red
O = [180, 180, 180]  # White
B = [0,0,0] # Black
w, h = 8, 8

class Piece:

    def __init__(self, game_matrix):
	self.hasSpace = False

    self.structure = [(0,0), (0,1), (1,0), (1,1)] # set of points of the piece, relative to row and col positions
	
    # TODO: Check if I can put the piece in the matrix
    self.row = 0
    self.oldrow = 0
    self.col = 2
    self.oldcol = 2

    def hasLanded(self, game_matrix, led_matrix):
        for point in self.structure:
            cellBelowIndex = (self.row + point[0] + 1, [self.col + point[1])
            if(cellBelowIndex[0] == 6):
                 return True
            if(game_matrix[cellBelowIndex[0]][cellBelowIndex[1]] == 1):
                if not (cellBelowIndex[0], cellBelowIndex[1]) in self.structure:
                    return True
        return False

    def canMoveLeft(self):
        for point in self.structure:
            cellLeftIndex = (self.row + point[0], [self.col + point[1] - 1)
            if(cellLeftIndex[1] <= 0):
                 return False
            if(game_matrix[cellBelowIndex[0]][cellBelowIndex[1]] == 1):
                if not (cellBelowIndex[0], cellBelowIndex[1]) in self.structure:
                    return False
        return True

    def canMoveRight(self):
        for point in self.structure:
            cellRightIndex = (self.row + point[0], [self.col + point[1] + 1)
            if(cellLeftIndex[1] >= 7):
                 return False
            if(game_matrix[cellBelowIndex[0]][cellBelowIndex[1]] == 1):
                if not (cellBelowIndex[0], cellBelowIndex[1]) in self.structure:
                    return False
        return True

    def rotate(self):
        pass # a square remains the same

    def paint(self, game_matrix, led_matrix): # Square block
        for point in self.structure: # Remove old from matrices
            oldCellIndex = (self.oldrow + point[0], [self.oldcol + point[1])
            game_matrix[oldCellIndex[0]][oldCellIndex[1]] = 0
            led_matrix[((oldCellIndex[0]) * 8) + oldCellIndex[1]] = B;
        
        for point in self.structure: # Add new to matrices
            cellIndex = (self.row + point[0], [self.col + point[1])
            game_matrix[cellIndex[0]][cellIndex[1]] = 1
            led_matrix[((cellIndex[0]) * 8) + cellIndex[1]] = O;
        
	    # Update old row and col positions	
	    self.oldrow = self.row
	    self.oldcol = self.col

class Matrix:
    
    def __init__(self):
        self.game_matrix = [[0 for x in range(w)] for y in range(h)] # Init game matrix state
        self.led_matrix = [B for x in range(h*w)] # Init led matrix state (array of 64 entries)
	self.piece = Piece(self.game_matrix)
    def invalidate(self):
        sense.set_pixels(self.led_matrix);

    def deleteRow(self, i):
        for j in range(i, 0, -1): # i i-1 ... 1
            for k in range(0, w):
            	self.game_matrix[j][k] = self.game_matrix[j - 1][k]
		self.led_matrix[j*8 + k] = self.led_matrix[(j-1)*8 + k]

    def clearRows(self):
        for i in range(1, h):
            delete = 1
            for j in range(0, w):
                if(delete != self.game_matrix[i][j] ):
                    delete = 0
                    break
            if delete:
                self.deleteRow(i)
        
    def tick(self):
        if self.piece is not None:
        	if(not (self.piece.hasLanded(self.game_matrix, self.led_matrix))):
 	            self.piece.row = self.piece.row + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
       		else:
                    self.clearRows()
                    self.piece = Piece(self.game_matrix)
		    if not self.piece.hasSpace:
			sense.show_message("Looooser", scroll_speed=0.04)
			sys.exit(0)
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()

    def movePiece(self, event):
        if(event.action == "pressed"):
            if(event.direction == "left"):
                if(self.piece.canMoveLeft()):
                    self.piece.col = self.piece.col - 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
            elif(event.direction == "right"):
                if(self.piece.canMoveRight()):
                    self.piece.col = self.piece.col + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
            elif(event.direction == "down"):
                if(not (self.piece.hasLanded(self.game_matrix, self.led_matrix))):
                    self.piece.row = self.piece.row + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()      
def tick_action (matrix): # To be repeated every 1 sec
    delay = 1
    while True:
    	time.sleep(delay);
        matrix.tick()        
    	
def stick_action(matrix):
    global sense
    
    while True:
        event = sense.stick.wait_for_event()
 #       print("The joystick was {} {}".format(event.action, event.direction))
        matrix.movePiece(event)
        
def start_stick(matrix):
    try:
        thread.start_new_thread( stick_action, (matrix,) )
    except Exception as err:
        print "Error: unable to start thread"
	print err

def start_timer(matrix):
    try:
        thread.start_new_thread( tick_action, (matrix,) )
    except Exception as err:
        print "Error: unable to start thread"
	print err

def start_game ():
    matrix = Matrix()
    #sense.show_message("Diningphil Tetris", scroll_speed=0.03)
    start_timer(matrix)
    start_stick(matrix)
    while True:
	pass
	
start_game();
