from sense_hat import SenseHat
import thread
import time

sense = SenseHat()
sense.set_rotation(180)



X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White
B = [0,0,0] # Black
w, h = 8, 8

game_matrix = [[0 for x in range(w)] for y in range(h)] # Init game matrix state
led_matrix = [B for x in range(h*w)] # Init led matrix state (array of 64 entries)

class Piece:
    def __init__(self):
        self.row = 1; # Positions can go from 1 to 8
        self.col = 4; # Positions can go from 1 to 8
        self.oldrow = 1;
        self.oldcol = 4;

    def hasLanded(self):
        return ((self.row == 7) or
               (game_matrix[self.row + 1] [self.col - 1] == 1) or
               (game_matrix[self.row + 1] [self.col] == 1))

    def paint(self): # Square block
	global game_matrix
	global led_matrix
        # Hard coded: remove matrix
        game_matrix[self.oldrow - 1][self.oldcol - 1] = 0;
        game_matrix[self.oldrow - 1] [self.oldcol] = 0;
        game_matrix[self.oldrow] [self.oldcol - 1] = 0;
        game_matrix[self.oldrow] [self.oldcol] = 0;
        
        led_matrix[((self.oldrow - 1 ) * 8) + self.oldcol] = B;
        led_matrix[((self.oldrow - 1 ) * 8) + self.oldcol + 1] = B;
        led_matrix[((self.oldrow) * 8) + self.oldcol] = B;
        led_matrix[((self.oldrow) * 8) + self.oldcol + 1] = B;

        # Hard coded: add matrix
        game_matrix[self.row - 1] [self.col - 1] = 1;
        game_matrix[self.row - 1] [self.col] = 1;
        game_matrix[self.row] [self.col - 1] = 1;
        game_matrix[self.row] [self.col] = 1;
        
        led_matrix[((self.row - 1 ) * 8) + self.col] = O;
        led_matrix[((self.row - 1 ) * 8) + self.col + 1] = O;
        led_matrix[((self.row) * 8) + self.col] = O;
        led_matrix[((self.row) * 8) + self.col + 1] = O;
	
	# Update old row and col positions	
	self.oldrow = self.row
	self.oldcol = self.col

        invalidate_Led_Matrix();

piece = Piece()

def tick_action (): # To be repeated every 1 sec
    global piece
    delay = 1;
    while True:
    	print "Tick"
    	time.sleep(delay);
    	if piece is not None:
        	if(not (piece.hasLanded()) ):
			print "Move piece"
 	           	piece.row = piece.row + 1
       		     	piece.paint()
       		else:
                    piece = Piece()
                    piece.paint()

def start_timer ():
    try:
        thread.start_new_thread( tick_action, () )
    except Exception as err:
        print "Error: unable to start thread"
	print err

def start_game ():
        piece = Piece()
        #sense.show_message("Diningphil Tetris", scroll_speed=0.03)
        start_timer()
	while True:
	   pass
def invalidate_Led_Matrix ():
    print "Called invalidate"
    sense.set_pixels(led_matrix);

start_game();
