

#! move to components once completed

class Phoneme:
    """
    A class which represents a stressed phoneme by using its ARPABET string
    and a stress value. It contains a method to calculate the distance
    between two Phonemes
    """
    def __init__(self, string:str="", stress:int=-1):
        self.string:str = string
        
        # if there is no stress (i.e. consonant) this is -1
        self.stress:int = stress
    
    def __str__(self):
        if self.stress != -1:
            return f"{self.string}{self.stress}"
        else:
            return self.string
            
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash((self.string, self.stress))

    def __eq__(self, other):
        return (self.string, self.stress) == (other.string, other.stress)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def distance(self, other:"Phoneme"):
        # this method necessarily needs to be symmetric
        
        if self == other:
            return 0
        
        #! temp
        elif self.string == other.string:
            return 1
        else:
            return 100
        
        # calculate the difference in the string 
        
        
        # calculate the difference in the stress
        
