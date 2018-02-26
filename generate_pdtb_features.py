

class PDTBFeatures:
    
 
    def __init__(self):
        
        # load the PDTB outputs --
        self.mainPath = "./auto-grader/ArgumentDetection/"
        self.pdtbInput = 'data/pdtb/input/'

        expansionFile = open( self.mainPath  + self.pdtbInput + 'expansion_sr.op')
        self.expansions = expansionFile.readlines()
        
        contingencyFile = open( self.mainPath  + self.pdtbInput + 'contingency_sr.op')
        self.contigencies = contingencyFile.readlines()
    
        comparisonFile = open( self.mainPath  + self.pdtbInput + 'comparison_sr.op')
        self.comparisons = comparisonFile.readlines()
    
    def returnPDTBOps(self,position):
        
        featureMap = {} 
        
        featureMap["PDTB_EXPANSION"] = self.expansions[position].strip()
        featureMap["PDTB_COMPARISON"] = self.comparisons[position].strip()
        featureMap["PDTB_CONTINGENCY"] = self.contigencies[position].strip()
        
        return featureMap
                                                            
                                                            