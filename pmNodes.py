class article:
    def __init__(self, ID):
        self.ID = ID
        self.authorList = [] # list of author objects
        self.title = None  
        self.citationsByID = []
    def numConnections_Cited(self):
        self.quantityConnections = len(citationsByID)
        return(self.quantityConnections)

class author:
    def __init__(self, ID):
        self.ID = ID
        self.name = None
        self.affiliation = None # list of institution objects

class institution:
    def __init__(self, ID):
        self.ID = ID
        self.name = None
        