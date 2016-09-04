# from sense import SenseHat
from threading import Thread
import time
import signal
import sys
from pythonsensehat.sense_hat.sense_hat import SenseHat
import shapes

sense = SenseHat()
#sense.set_rotation(180)


X = [255, 0, 0]  # Red
O = [180, 180, 180]  # White
B = [0,0,0] # Black
w, h = 8, 8
score = 0
quit = False

class Matrix:

    def __init__(self):
        self.game_matrix = [[0 for x in range(w)] for y in range(h)] # Init game matrix state
        self.led_matrix = [B for x in range(h*w)] # Init led matrix state (array of 64 entries)
	self.piece = shapes.pickRandomPiece()    
        
    def invalidate(self):
        sense.set_pixels(self.led_matrix);

    def paintPiece(self): # Square block
        for point in self.piece.oldstructure: # Remove old from matrices
            oldCellIndex = (self.piece.oldrow + point[0], self.piece.oldcol + point[1])
            self.game_matrix[oldCellIndex[0]][oldCellIndex[1]] = 0
            self.led_matrix[((oldCellIndex[0]) * 8) + oldCellIndex[1]] = B;
        
        for point in self.piece.structure: # Add new to matrices
            cellIndex = (self.piece.row + point[0], self.piece.col + point[1])
            self.game_matrix[cellIndex[0]][cellIndex[1]] = 1
            self.led_matrix[((cellIndex[0]) * 8) + cellIndex[1]] = O;
        
    	# Update old row and col positions	
	    self.piece.oldrow = self.piece.row
	    self.piece.oldcol = self.piece.col
	    self.piece.oldstructure = self.piece.structure

    def deleteRow(self, i):
        for j in range(i, 0, -1): # i i-1 ... 1
            for k in range(0, w):
            	self.game_matrix[j][k] = self.game_matrix[j - 1][k]
		self.led_matrix[j*8 + k] = self.led_matrix[(j-1)*8 + k]

    def clearRows(self):
        global score
        for i in range(1, h):
            delete = 1
            for j in range(0, w):
                if(delete != self.game_matrix[i][j] ):
                    delete = 0
                    break
            if delete:
                score = score + 1
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

    def findSpaceForPiece(self, piece):
        piece.row = 0
        piece.oldrow = 0
        for i in range(0, 7):
             piece.col = i
             piece.col = i
             fits = True
             for point in piece.structure:
                 cellIndex = (piece.row + point[0], piece.col + point[1])
                 if cellIndex[1] > 7 or (self.game_matrix[cellIndex[0]][cellIndex[1]] == 1):
                     fits = False
                     break
             if fits:
                 return True
        return False

    
    def tick(self):
        if self.piece is not None:
        	if(not (self.hasLanded())):
 	            self.piece.row = self.piece.row + 1
                    self.paintPiece()
                    self.invalidate()
       		else:
                    self.piece = None
                    self.clearRows()
                    p = shapes.pickRandomPiece() 
		    if not self.findSpaceForPiece(p):
			return False
                    self.piece = p
                    self.paintPiece()
                    self.invalidate()
	return True

    def movePiece(self, event):
        if self.piece is None:
            return
        if(event.action == "pressed"):
            if(event.direction == "left"):
	        if(self.canMoveLeft()):
		    self.piece.col = self.piece.col - 1
                    self.paintPiece()
                    self.invalidate()
            elif(event.direction == "right"):
                if(self.canMoveRight()):
                    self.piece.col = self.piece.col + 1
                    self.paintPiece()
                    self.invalidate()
	    elif(event.direction == "up"):
                if(self.canRotate()):
                    self.piece.rotate()
                    self.paintPiece()
                    self.invalidate()
            elif(event.direction == "down"): 
                if(not (self.hasLanded())):
                    self.piece.row = self.piece.row + 1
                    self.paintPiece()
                    self.invalidate()

    def canRotate(self):
        row = self.piece.row
        col = self.piece.col
        struct = self.piece.getNextStructure()
        fits = True
        for point in struct:
                 cellIndex = (row + point[0], col + point[1])
		 try:
                     if cellIndex[1] > 7 or cellIndex[0] > 7 or (self.game_matrix[cellIndex[0]][cellIndex[1]] == 1 and not (point[0], point[1]) in self.piece.structure) :
                     	fits = False
		     	#print "Cannot rotate ",  (point[0], point[1] - 1) in self.piece.structure, (point[0], point[1] - 1), self.piece.structure
                        break
		 except Exception as err:
			print "Cellindex is ", cellIndex                 
        return fits
    
def tick_action (matrix): # To be repeated every 1 sec
    delay = 1
    global score
    global quit
    print "Started tick thread"
    while not quit:
    	time.sleep(delay);
	try:
	    if not quit:
		if not matrix.tick():
                	sense.show_message("Final score: " + str(score), scroll_speed=0.07)
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
            event = sense.stick.wait_for_event(timeout=1)
#           print("The joystick was {} {}".format(event.action, event.direction))	
	    if event is not None:
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
