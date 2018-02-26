import nltk
from sets import Set

class SyntacticFeatures:
    def __init__(self):
        self.POSList = ["SBAR","SBARQ","SINV","SQ","S","FRAG"]
        self.POSList = ["sbar","sbarq","sinv","sq","s","frag"]

        self.PresentList = ["VBP","VBZ","VB"]
        self.PresentList = ["vbp","vbz"]
        
        self.PastList = ["VBD"]
        self.PastList = ["vbd"]
        
        #run a preprocessing on top of all sentences to capture the tense (root) form
        
        mainPath = "./auto-grader/ArgumentDetection/"
        
    def setPDTBRelationProductionFile(self,productionFile,relation):
        
        self.productionFile = productionFile
        self.sourceTrainingProductions, self.targetTrainingProductions = self.prod_pdtb_relation_read_from_file(self.productionFile,relation)
        
        self.sourceTrainingProductions.extend(Set(self.targetTrainingProductions))
        self.trainingProductions = Set(self.sourceTrainingProductions)

        

    def setRelationProductionFile(self,productionFile):
        self.productionFile = productionFile
        self.sourceTrainingProductions, self.targetTrainingProductions = self.prod_sr_relation_read_from_file(self.productionFile)
        
        self.sourceTrainingProductions.extend(Set(self.targetTrainingProductions))
        self.trainingProductions = Set(self.sourceTrainingProductions)

    def setProductionFile(self, productionFile):
        self.productionFile = productionFile
        self.trainingProductions = self.prod_read_from_file(self.productionFile)
        
    def setSourceProductionFile(self, productionFile):
        self.productionFile = productionFile
        self.sourceTrainingProductions = self.prod_read_from_file(self.productionFile)
        
    def setTargetProductionFile(self, productionFile):
        self.productionFile = productionFile
        self.targetTrainingProductions = self.prod_read_from_file(self.productionFile)
    
    def getSourceProductionFeats(self):
        return self.trainingProductions
    
   # def getTargetProductionFeats(self):
   #     return self.targetTrainingProductions
    
    def getProductionFeats(self):
        return self.trainingProductions
     
         
    def prod_read_from_file(self,filename):
        f = open(filename,"r")
        lines = f.readlines()
        productions = Set()
        for index in range(1,len(lines)): # 0 is the header
            line = lines[index]
            prodText = line.split('\t')[2]
            allProds = self.createProductions(prodText)
            productions.update(Set(allProds))
        f.close()
        return list(productions)

     
    def prod_relation_read_from_file(self,filename):
        f = open(filename,"r")
        lines = f.readlines()
        source_productions = Set()
        target_productions = Set()

        for index in range(1,len(lines)): # 0 is the header
            line = lines[index]
            sourceProdText = line.split('\t')[2]
            sourceProdText = sourceProdText[1:len(sourceProdText)]
            allSourceProds = self.createProductions(sourceProdText)
            source_productions.update(Set(allSourceProds))
            
            targetProdText = line.split('\t')[3]
            targetProdText = targetProdText[1:len(targetProdText)]
            allTargetProds = self.createProductions(targetProdText)
            target_productions.update(Set(allTargetProds))
        f.close()
        return list(source_productions),list(target_productions)
    
    def prod_pdtb_relation_read_from_file(self,filename,relation):
       
        f = open(filename,"r")
        lines = f.readlines()
        source_productions = Set()
        target_productions = Set()

        for index in range(1,len(lines)): # 0 is the header
            line = lines[index]
            features = line.split('\t')
            if not features[2].lower().startswith(relation):
                continue 
            
            sourceProdText = line.split('\t')[3] # always check the splits 
            sourceProdText = sourceProdText[1:len(sourceProdText)-1]
            allSourceProds = self.createProductions(sourceProdText)
            source_productions.update(Set(allSourceProds))
            
            targetProdText = line.split('\t')[4]
            targetProdText = targetProdText[1:len(targetProdText)-1]
            allTargetProds = self.createProductions(targetProdText)
            target_productions.update(Set(allTargetProds))
        f.close()
        return list(source_productions),list(target_productions)

    
    def prod_sr_relation_read_from_file(self,filename):
        f = open(filename,"r")
        lines = f.readlines()
        source_productions = Set()
        target_productions = Set()

        for index in range(1,len(lines)): # 0 is the header
            line = lines[index]
            sourceProdText = line.split('\t')[3] # always check the splits 
            sourceProdText = sourceProdText[1:len(sourceProdText)-1]
            allSourceProds = self.createProductions(sourceProdText)
            source_productions.update(Set(allSourceProds))
            
            targetProdText = line.split('\t')[4]
            targetProdText = targetProdText[1:len(targetProdText)-1]
            allTargetProds = self.createProductions(targetProdText)
            target_productions.update(Set(allTargetProds))
        f.close()
        return list(source_productions),list(target_productions)

    
    def createProductions(self,prodText):
        
        productions = []
        prodText = prodText[0:len(prodText)-1]
        features = prodText.split(',') 
        
        for feature in features:
            feature = feature.strip() 
            productions.append("PROD" + "|||" + feature);
        return productions
    
    
    def get_productions(self,production):
        productionFeatures = {}
        
        allProds = self.createProductions(production)
        
        for prod in allProds:
            if prod in self.trainingProductions:
                old = productionFeatures.get(prod)
                if old is None:
                    old = 0 
                productionFeatures[prod] = old+1
        
        return productionFeatures
    
    def get_rel_productions(self,production,type):
        productionFeatures = {}
        allProds = self.createProductions(production)
        
   #     self.trainingProductions = self.sourceTrainingProductions
        
        for prod in allProds:
            if prod in self.trainingProductions:
                old = productionFeatures.get(prod)
                if old is None:
                    old = 0 
                productionFeatures[prod] = old+1
        
        return productionFeatures

    def get_subclauses(self,clause):
        subclause_count = 0
        pos_index = 0
        while clause.find(self.POSList[pos_index]) == -1:
            pos_index +=1
            if pos_index == len(self.POSList):
                return 0
        if pos_index < len(self.POSList):
            index = clause.find(self.POSList[pos_index])
            while index != -1:
                subclause_count += 1
                index = clause.find("("+self.POSList[pos_index],index+1)
            return float(subclause_count)

    def get_depth(self,clause):
        max_depth = 0
        depth = -1
        for char in clause:
            if char == "(":
                depth += 1
            elif char == ")":
                if max_depth < depth:
                    max_depth = depth
                depth -= 1
        return float(max_depth)

    def is_present_tense(self,clause,deptree):
        
        #first search for root
        relations = deptree.split()
        present = False 
        past = False
        root = False 
        for relation in relations:
            tokens = relation.lower().split('|')
            word = tokens[0]
            pos = tokens[1]
            chunk = tokens[2]
            grammar = tokens[3]
            if grammar == 'root':
                if pos.startswith('v'):
                    root = True
            
            if pos in self.PresentList:
                present = True
                if grammar == 'root':
                    return 2.0
            if pos in self.PastList:
                past = True
                if grammar == 'root':
                    return 1.0 
        
        #if we are here then we have not found root or the POS as verb --
        #in that case - just return any verb if we found as present or past list 
        '''
        verb_index = clause.find("(vp") 
        main_verb = clause.find("(v",verb_index+1)
        if main_verb > -1:
            if clause[main_verb:clause.find(" ",main_verb)] in self.PresentList:
                return 1
        '''
        if present == True and root == False:
            return 2.0
        if past == True and root == False:
            return 1.0
                
        return 0



