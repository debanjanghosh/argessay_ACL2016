import nltk

class IndicatorFeatures:
    def __init__(self):
        self.first_person = ["FP|||i","FP|||me","FP|||my","FP|||mine","FP|||myself"]

    def setDiscourseMarkers(self, markerFile):
        self.discourse_markers = []
        self.source_discourse_markers = []
        self.target_discourse_markers = []
        
        
        f = open(markerFile,"r")
        for line in f:
            self.discourse_markers.append('DISCOURSE'+'|||'+line.strip().lower())
            self.source_discourse_markers.append('SOURCE|||DISCOURSE'+'|||'+line.strip().lower())
            self.target_discourse_markers.append('TARGET|||DISCOURSE'+'|||'+line.strip().lower())

        f.close()

    
    def getFirstPersonFeats(self):
        return self.first_person
    
    def getSourceDiscourseFeats(self):
        return self.source_discourse_markers
    
    def getTargetDiscourseFeats(self):
        return self.target_discourse_markers
    
    def getDiscourseFeats(self):
        return  self.discourse_markers
    
    def get_type_discourse_marker(self,clause,sentence,type):
        
        if type == 'SOURCE':
            testDiscourseMarkers = self.source_discourse_markers
        if type == 'TARGET':
            testDiscourseMarkers = self.target_discourse_markers
            
        index = sentence.find(clause)
        if index != -1:
            preceding_sent = sentence[:index]
            discourse = {}
            words = nltk.word_tokenize(preceding_sent)
            for word in words:
                wordTag = type + '|||' + 'DISCOURSE'+'|||' + word.lower() 
                if wordTag in testDiscourseMarkers:
                    old = discourse.get(wordTag)
                    if old is None:
                        old = 0
                    discourse[wordTag] = old+1
                    
        return discourse

    def get_implicit_type_discourse_marker(self,clause,type):
        
        if type == 'SOURCE':
            testDiscourseMarkers = self.source_discourse_markers
        if type == 'TARGET':
            testDiscourseMarkers = self.target_discourse_markers
            
        discourse = {}
        words = nltk.word_tokenize(clause.lower())
        for word in words:
            wordTag = type + '|||' + 'DISCOURSE'+'|||' + word.lower() 
            if wordTag in testDiscourseMarkers:
                old = discourse.get(wordTag)
                if old is None:
                    old = 0
                discourse[wordTag] = old+1
                    
        return discourse

    
    def get_discourse_marker(self,clause,sentence):
        index = sentence.find(clause)
        if index != -1:
            preceding_sent = sentence[:index]
            discourse = {}
            words = nltk.word_tokenize(preceding_sent)
            for word in words:
                wordTag = 'DISCOURSE'+'|||' + word.lower() 
                if wordTag in self.discourse_markers:
                    old = discourse.get(wordTag)
                    if old is None:
                        old = 0
                    discourse[wordTag] = old+1
                    
        return discourse

    def get_first_person(self,sent):
        firstPersons = {}
        words = nltk.word_tokenize(sent)
        for word in words:
            
            tag = 'FP' + '|||' + word.strip().lower()
            if tag in self.first_person:
                old = firstPersons.get(tag)
                if old is None :
                    old = 0
                firstPersons[tag] = old+1
                
        return firstPersons
