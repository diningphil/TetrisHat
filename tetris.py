from sense_hat import SenseHat
from threading import Thread
import time
import signal
import sys

sense = SenseHat()
#sense.set_rotation(180)


X = [255, 0, 0]  # Red
O = [180, 180, 180]  # White
B = [0,0,0] # Black
w, h = 8, 8
quit = False

class Piece:

    def __init__(self, game_matrix):
	self.hasSpace = False
        self.structure = [(0,0), (0,1), (1,0), (1,1)] # set of points of the piece, relative to row and col positions
	
        # TODO: Check if I can put the piece in the matrix
        self.row = 0
        self.oldrow = 0
        self.col = 2
        self.oldcol = 2
        self.hasSpace = True

    def rotate(self):
        pass # a square remains the same

    def paint(self, game_matrix, led_matrix): # Square block
        for point in self.structure: # Remove old from matrices
            oldCellIndex = (self.oldrow + point[0], self.oldcol + point[1])
            game_matrix[oldCellIndex[0]][oldCellIndex[1]] = 0
            led_matrix[((oldCellIndex[0]) * 8) + oldCellIndex[1]] = B;
        
        for point in self.structure: # Add new to matrices
            cellIndex = (self.row + point[0], self.col + point[1])
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
    
    def hasLanded(self):
        for point in self.piece.structure:
            if(self.piece.row + point[0] == 7):
                 return True
            cellBelowIndex = (self.piece.row + point[0] + 1, self.piece.col + point[1])
            if(self.game_matrix[cellBelowIndex[0]][cellBelowIndex[1]] == 1):
                if not (point[0] + 1, point[1]) in self.piece.structure: # that's not my point
                    return True
        return False

    def canMoveLeft(self):
        for point in self.piece.structure:
            if(self.piece.col + point[1] == 0):
                 return False
            cellLeftIndex = (self.piece.row + point[0], self.piece.col + point[1] - 1)
            if(self.game_matrix[cellLeftIndex[0]][cellLeftIndex[1]] == 1):
                if not (point[0], point[1] - 1) in self.piece.structure:
                    return False
        return True

    def canMoveRight(self):
        for point in self.piece.structure:
            if(self.piece.col + point[1] == 7):
                 return False
            cellRightIndex = (self.piece.row + point[0], self.piece.col + point[1] + 1)
            if(self.game_matrix[cellRightIndex[0]][cellRightIndex[1]] == 1):
                if not (point[0], point[1] + 1) in self.piece.structure:
                    return False
        return True

    def tick(self):
        if self.piece is not None:
        	if(not (self.hasLanded())):
 	            self.piece.row = self.piece.row + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
       		else:
                    self.clearRows()
                    self.piece = Piece(self.game_matrix)
		    if not self.piece.hasSpace:
			return False
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
	return True

    def movePiece(self, event):
        if(event.action == "pressed"):
            if(event.direction == "left"):
	        if(self.canMoveLeft()):
		    self.piece.col = self.piece.col - 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
            elif(event.direction == "right"):
                if(self.canMoveRight()):
                    self.piece.col = self.piece.col + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
            elif(event.direction == "down"):
                if(not (self.hasLanded())):
                    self.piece.row = self.piece.row + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()      

def tick_action (matrix): # To be repeated every 1 sec
    delay = 1
    global quit
    print "Started tick thread"
    while not quit:
    	time.sleep(delay);
	try:
	    if not quit:
		if not matrix.tick():
                	sense.show_message("Looser", scroll_speed=0.03)
                	quit = True
	except Exception as err:
	    print err
	    quit = True
    
def stick_action(matrix):
    global sense
    global quit
    print "Started stick event listener"
    while not quit:
	try:
            event = sense.stick.wait_for_event()
#           print("The joystick was {} {}".format(event.action, event.direction))	
	    matrix.movePiece(event)
	except Exception as err:
            print err
            quit = True
      
def sig_handler(signal, frame):
	global quit
	print "SIGINT captured"
	sense.clear()
	quit = True # Problem: stick can be waiting for event, need send an event
	sys.exit(0)    

signal.signal(signal.SIGINT, sig_handler)

def start_game ():

    matrix = Matrix()

    thread = Thread(target = tick_action, args = (matrix, ))
    thread2 = Thread(target = stick_action, args = (matrix, ))
    thread.start()
    thread2.start()

    while not quit:
	time.sleep(1)


start_game();
