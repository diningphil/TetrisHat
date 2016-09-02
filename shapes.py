import random

class Piece:

    def __init__(self):
        structure = None
        self.row = 0
        self.oldrow = 0
        self.col = 0
        self.oldcol = 0

    def rotate(self):
        raise NotImplementedError("Please implement this method")

class Square(Piece):
    structure = [(0,0), (0,1), (1,0), (1,1)]	

    def rotate(self):
        pass

class JPiece(Piece):
    structure = [(0,0), (0,1), (1,1), (1,2)]

    def rotate(self):
        pass

def pickRandomPiece():
    randomIndex = random.randint(0,1)
    if(randomIndex == 0):
        return Square()
    elif(randomIndex == 1):
        return JPiece()
    return Piece() 
