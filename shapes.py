import random

class Piece:

    def __init__(self):
        self.idxRot = 0
        self.structure = None
        self.oldstructure = None
        self.row = 0
        self.oldrow = 0
        self.col = 0
        self.oldcol = 0

    def rotate(self):
        self.idxRot = (self.idxRot + 1) % 4
        if(self.idxRot == 0):
            self.structure = self.standardRotation()
        elif(self.idxRot == 1):
            self.structure = self.rotateRight()
        elif(self.idxRot == 2):
            self.structure = self.flip()
        elif(self.idxRot == 2):
            self.structure = self.rotateLeft()
            
        
    def rotateLeft(self):
        raise Exception("Implement it")
    def rotateRight(self):
        raise Exception("Implement it")
    def standardRotation(self):
        raise Exception("Implement it")
    def flip(self):
        raise Exception("Implement it")
    

class Square(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        self.structure = [(0,0), (0,1), (1,0), (1,1)]	

    def rotateLeft(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def rotateRight(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def standardRotation(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def flip(self):
        return [(0,0), (0,1), (1,0), (1,1)]	

class JPiece(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        self.structure = [(0,0), (0,1), (1,1), (1,2)]

    def rotateLeft(self):
        return [(0,1), (1,1), (1,0), (2,0)]	
    def rotateRight(self):
        return [(0,1), (1,1), (1,0), (2,0)]	
    def standardRotation(self):
        return [(0,0), (0,1), (1,1), (1,2)]
    def flip(self):
        return [(1,0), (1,1), (0,1), (0,2)]	
     
    def pickRandomPiece():
        randomIndex = random.randint(0,1)
        if(randomIndex == 0):
            return Square()
        elif(randomIndex == 1):
            return JPiece()
        return Piece() 
