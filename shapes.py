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
        self.structure = self.getNextStructure()

    def getNextStructure(self):
        if(self.idxRot == 0):
            return self.standardPosition()
        elif(self.idxRot == 1):
            return self.rotateRight()
        elif(self.idxRot == 2):
            return = self.flip()
        elif(self.idxRot == 3):
            return self.rotateLeft()

    def standardPosition(self):
        raise Exception("Implement it")
    def rotateLeft(self):
        raise Exception("Implement it")
    def rotateRight(self):
        raise Exception("Implement it")
    def flip(self):
        raise Exception("Implement it")
    

class Square(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        self.structure = [(0,0), (0,1), (1,0), (1,1)]
        self.oldstructure = [(0,0), (0,1), (1,0), (1,1)]	

    def standardPosition(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def rotateLeft(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def rotateRight(self):
        return [(0,0), (0,1), (1,0), (1,1)]	
    def flip(self):
        return [(0,0), (0,1), (1,0), (1,1)]	

class JPiece(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        self.structure = [(0,0), (0,1), (1,1), (1,2)]
        self.oldstructure = [(0,0), (0,1), (1,1), (1,2)]

    def standardPosition(self):
        return [(0,0), (0,1), (1,1), (1,2)]
    def rotateLeft(self):
        return [(0,1), (1,1), (1,0), (2,0)]	
    def rotateRight(self):
        return [(0,1), (1,1), (1,0), (2,0)]	
    def flip(self):
        return [(1,0), (1,1), (0,1), (0,2)]	

class Stick(Piece):
    
    def __init__(self):
        Piece.__init__(self)
        self.structure = [(0,0), (0,1), (0,2)]
        self.oldstructure = [(0,0), (0,1), (0,2)]

    def standardPosition(self):
        return [(0,0), (0,1), (0,2)]
    def rotateLeft(self):
        return [(0,1), (1,1), (2,1)]	
    def rotateRight(self):
        return [(0,1), (1,1), (2,1)]	
    def flip(self):
        return [(0,0), (0,1), (0,2)]	
     
def pickRandomPiece():
        randomIndex = random.randint(0,2)
        if(randomIndex == 0):
	    print "Picked Square"
            return Square()
        elif(randomIndex == 1):
	    print "Picked JPiece"
            return JPiece()
        elif(randomIndex == 1):
	    print "Picked Stick"
            return Stick()
        return Square() 

