from sense_hat import SenseHat
import thread
import time
import signal
import sys

sense = SenseHat()
sense.set_rotation(180)

def sig_handler(signal, frame):
    sense.clear()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White
B = [0,0,0] # Black
w, h = 8, 8

class Piece:
    def __init__(self):
        self.row = 0; # Positions can go from 0 to 7
        self.col = 0; # Positions can go from 0 to 7
        self.oldrow = 0;
        self.oldcol = 0;

    def hasLanded(self, game_matrix, led_matrix):
        return ((self.row == 6) or
               (game_matrix[self.row + 2] [self.col] == 1) or
               (game_matrix[self.row + 2] [self.col + 1] == 1))

    def canMoveLeft(self):
        return self.row > 1
    def canMoveRight(self):
        return self.row < 6
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
        self.piece = Piece()
        self.game_matrix = [[0 for x in range(w)] for y in range(h)] # Init game matrix state
        self.led_matrix = [B for x in range(h*w)] # Init led matrix state (array of 64 entries)

    def invalidate(self):
        self.piece.paint(self.game_matrix, self.led_matrix)
        sense.set_pixels(self.led_matrix);

    def tick(self):
        if self.piece is not None:
        	if(not (self.piece.hasLanded(self.game_matrix, self.led_matrix))):
 	            self.piece.row = self.piece.row + 1
                    self.piece.paint(self.game_matrix, self.led_matrix)
                    self.invalidate()
       		else:
                    print "New Piece"
                    self.piece = Piece()
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
        
def tick_action (matrix): # To be repeated every 1 sec
    delay = 1
    while True:
    	time.sleep(delay);
        matrix.tick()        
    	
def stick_action(matrix):
    global sense
    
    print "Listening to stick"
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
