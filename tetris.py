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
	for i in range(0,w-1):
		if(game_matrix[0][i] == 0 and game_matrix[0][i+1] == 0
		   and game_matrix[1][i] == 0 and game_matrix[1][i+1] == 0):
			self.hasSpace = True
			self.row = 0; # Positions can go from 0 to 7
       			self.col = i; # Positions can go from 0 to 7
        		self.oldrow = 0;
        		self.oldcol = i;
    def hasLanded(self, game_matrix, led_matrix):
        return ((self.row == 6) or
               (game_matrix[self.row + 2] [self.col] == 1) or
               (game_matrix[self.row + 2] [self.col + 1] == 1))

    def canMoveLeft(self):
        return self.col > 0

    def canMoveRight(self):
        return self.col < 6

    def rotate(self):
        pass # a square remains the same

    def paint(self, game_matrix, led_matrix): # Square block
	
        # Hard coded: remove matrix
        game_matrix[self.oldrow][self.oldcol] = 0;
        game_matrix[self.oldrow] [self.oldcol + 1] = 0;
        game_matrix[self.oldrow + 1] [self.oldcol] = 0;
        game_matrix[self.oldrow + 1] [self.oldcol + 1] = 0;
        
        led_matrix[((self.oldrow) * 8) + self.oldcol] = B;
        led_matrix[((self.oldrow) * 8) + self.oldcol + 1] = B;
        led_matrix[((self.oldrow + 1) * 8) + self.oldcol] = B;
        led_matrix[((self.oldrow + 1) * 8) + self.oldcol + 1] = B;

        # Hard coded: add matrix
        game_matrix[self.row] [self.col] = 1;
        game_matrix[self.row] [self.col + 1] = 1;
        game_matrix[self.row + 1] [self.col] = 1;
        game_matrix[self.row + 1] [self.col + 1] = 1;
        
        led_matrix[((self.row) * 8) + self.col] = O;
        led_matrix[((self.row) * 8) + self.col + 1] = O;
        led_matrix[((self.row + 1) * 8) + self.col] = O;
        led_matrix[((self.row + 1) * 8) + self.col + 1] = O;
	
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
