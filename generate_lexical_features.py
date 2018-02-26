from nltk import bigrams,trigrams,word_tokenize
import nltk
from sets import Set
from _collections import defaultdict

#from nltk.tokenize import StanfordTokenizer
from nltk.tokenize import TreebankWordTokenizer

class LexicalFeatures:
    def __init__(self):
     #   self.VerbList = ["VP","VB","VBD","VBG","VBN","VBP","VBZ"]
     #   self.AdverbList = ["A    DVP","WHAVP","RB","RBR","RBS","WRB"]
        self.ngramTypes = ['unigram' , 'bigram', 'trigram', 'verb', 'adverb', 'modal','wordpair', 'firstthree','firstlast']
        self.Modal = "MD"
        mainPath = "./auto-grader/ArgumentDetection/"
        self.DF = 3
    
    def setDF(self,df):
        self.DF = df
    
    def setFileNames(self,unigrams,bigrams,trigrams,verbs,adverbs,modals):
        
        self.Unigrams = self.read_from_file(unigrams,self.ngramTypes[0],None)
        self.Bigrams = self.read_from_file(bigrams,self.ngramTypes[1],None)
        self.Trigrams = self.read_from_file(trigrams,self.ngramTypes[2],None)
        self.VerbList = self.read_from_file(verbs,self.ngramTypes[3],None)
        self.AdverbList = self.read_from_file(adverbs,self.ngramTypes[4],None)
        self.ModalList = self.read_from_file(modals,self.ngramTypes[5],None)
        
    def setModalFile(self,modals):
        self.ModalList = self.read_from_file(modals,self.ngramTypes[5],None)

        
    def setFirstLast(self,firstLastFile):    
        self.firstLast = self.read_from_file(firstLastFile, self.ngramTypes[8],None)
        print 'first last file is loaded'
    
    def setFirstThreeFile(self,firstThreeFile):
        self.firstThree = self.read_from_file(firstThreeFile, self.ngramTypes[7],None)
        print 'first three file is loaded'
    
    def setArgRelationWordPairFile(self,wordpairFile):
        self.allWordPairs = self.read_from_file(wordpairFile, self.ngramTypes[6],filter=self.DF)
        print 'wordpairs are loaded'
        
     #   self.modalFile = 
    
    def getFirstLastFeats(self):
        return self.firstLast
    
    def getFirstThirdFeats(self):
        return self.firstThree
    
    def getWordPairFeats(self):
        return self.allWordPairs
    
    def getModals(self):
        return self.ModalList

    def getVerbFeats(self):
        return  self.VerbList 

    def getAdverbFeats(self):
        return  self.AdverbList 

    def getUnigramFeats(self):
        return self.Unigrams 
    
    def getBigramFeats(self):
        return self.Bigrams 
    
    def getTrigramFeats(self):
        return self.Trigrams 
    
    def read_from_file(self,filename,type,filter):
        f = open(filename,"r")
        x_grams = {}
        for line in f:
            if filter is not None:
                if int (line.split("\t")[1]) >= int(filter):
                    x_grams[type + '|||' + line.split("\t")[0]] = line.split("\t")[1]
            else:
                x_grams[type + '|||' + line.split("\t")[0]] = line.split("\t")[1]
        f.close()
        return x_grams
    


    def count_tag(self,tag,clause):
        index = clause.find("("+tag+" ")
        count = 0
        while index != -1 and index < len(clause):
            count += 1
            index = clause.find("("+tag+" ",index+1)
        return float(count)

    ''' we are not taking the count of verbs -- need change in the function '''
    def get_verbs(self,clause):
        verbFeatures = {}
        
        postags = nltk.pos_tag(nltk.word_tokenize(clause.lower()) )
        for word,tag in postags:
            typeWord = self.ngramTypes[3] + '|||' + word
            if tag.startswith('V') and typeWord in self.VerbList:
                old = verbFeatures.get(typeWord)
                if old is None:
                    old = 0
                verbFeatures[typeWord] = old+1
                
        return verbFeatures

    def get_adverbs(self,clause):
        adVerbFeatures = {}
        postags = nltk.pos_tag(nltk.word_tokenize(clause.lower()))
        
        for word,tag in postags:
            typeWord = self.ngramTypes[4] + '|||' + word
            if 'RB' in tag and  typeWord in self.AdverbList:
                old = adVerbFeatures.get(typeWord)
                if old is None:
                    old = 0
                adVerbFeatures[typeWord] = old+1
                
        return adVerbFeatures

    def get_modals(self,clause):
        
        modalFeatures = {}
        postags = nltk.pos_tag(nltk.word_tokenize(clause.lower()))
        
        for word,tag in postags:
            typeWord = self.ngramTypes[5] + '|||' + word
            if 'MD' in tag and typeWord in self.ModalList:
                old = modalFeatures.get(typeWord)
                if old is None:
                    old = 0
                modalFeatures[typeWord] = old+1
                
        return modalFeatures


    def get_ngrams(self,sent):
        ngramFeatures = {}
        
        sent_list1 = word_tokenize(sent)
        unigramFeatures = self.check_belonging(sent_list1,self.Unigrams,self.ngramTypes[0])
        ngramFeatures.update(unigramFeatures)
        
        sent_list2 = bigrams(sent_list1)
        bigramFeatures = self.check_belonging(sent_list2,self.Bigrams,self.ngramTypes[1])
        ngramFeatures.update(bigramFeatures)

        sent_list3 = trigrams(sent_list1)
        trigramFeatures = self.check_belonging(sent_list3,self.Trigrams,self.ngramTypes[2])
        ngramFeatures.update(trigramFeatures)

        return ngramFeatures

    def createWordPairs(self,s_arg,t_arg):
        
        s_arg_tokens = word_tokenize(s_arg.lower())
        t_arg_tokens = word_tokenize(t_arg.lower())
        
        s_arg_tokens = TreebankWordTokenizer().tokenize(s_arg.lower())
        
        wps = ['wordpair' + '|||' + s_arg_token + '_' + t_arg_token for s_arg_token in s_arg_tokens for t_arg_token in t_arg_tokens]
     #   for s_arg_token in s_arg_tokens:
     #       for t_arg_token in t_arg_tokens:
     #           wp = s_arg_token + '_' + t_arg_token
      #          wps.append(wp)
        
        wpFeatures = self.check_belonging_wp(Set(wps), self.allWordPairs, self.ngramTypes[6])
        return wpFeatures
    
    def createFirstLastWords(self,source_arg,target_arg,source_sent,target_sent):
        
        fv = []
        tokens = []
   
        fv.append('SOURCE' + '|||' + nltk.word_tokenize(source_arg.lower())[0])
        fv.append('SOURCE' + '|||' + nltk.word_tokenize(source_sent.lower())[0])
        fv.append('SOURCE' + '|||' + nltk.word_tokenize(source_arg.lower())[-1])
        if len(source_sent) > 1:
            fv.append('SOURCE' + '|||' + nltk.word_tokenize(source_sent.lower())[-2])
        else:
            fv.append('SOURCE' + '|||' + nltk.word_tokenize(source_sent.lower())[-1])

            
        fv.append('TARGET' + '|||' + nltk.word_tokenize(target_arg.lower())[0])
        fv.append('TARGET' + '|||' + nltk.word_tokenize(target_sent.lower())[0])
        fv.append('TARGET' + '|||' + nltk.word_tokenize(target_arg.lower())[-1])
        if len(target_sent) > 1:
            fv.append('TARGET' + '|||' + nltk.word_tokenize(target_sent.lower())[-2])
        else:
            fv.append('TARGET' + '|||' + nltk.word_tokenize(target_sent.lower())[-1])
        
        ftFeatures = self.check_belonging(fv, self.firstLast, self.ngramTypes[8])
        return ftFeatures
   
    def createImplicitFirstLastWords(self,source_arg,target_arg):
        
        fv = []
        tokens = []
        PUNCTUATION = (';', ':', ',', '.', '!', '?')
        
        source_tokens =  nltk.word_tokenize(source_arg.lower())
        target_tokens = nltk.word_tokenize(target_arg.lower())
        
        fv.append('SOURCE' + '|||' + source_tokens[0])
        if  source_tokens[-1] not in PUNCTUATION:
            fv.append('SOURCE' + '|||' + source_tokens[-1])
        else:
             fv.append('SOURCE' + '|||' + source_tokens[-2])
        
        fv.append('TARGET' + '|||' + target_tokens[0])
        if  target_tokens[-1] not in PUNCTUATION:
            fv.append('TARGET' + '|||' + target_tokens[-1])
        else:
             fv.append('TARGET' + '|||' + target_tokens[-2])
       
        ftFeatures = self.check_belonging(fv, self.firstLast, self.ngramTypes[8])
        return ftFeatures

        
    def createFirstThirdWords(self,s_arg,t_arg):
        
        fv = []
        tokens = []
        s_arg_tokens = nltk.word_tokenize(s_arg.lower())
        t_arg_tokens = nltk.word_tokenize(t_arg.lower())
   
        for i in range(min(3,len(s_arg_tokens))):
            tokens.append(s_arg_tokens[i])
        
        fv.append( 'SOURCE' + '|||' + '_'.join(tokens) )
        tokens = []
        
        for i in range(min(3,len(t_arg_tokens))):
            tokens.append(t_arg_tokens[i])
      
        fv.append(  'TARGET' + '|||' + '_'.join(tokens) )
        
        
        
        ftFeatures = self.check_belonging(fv, self.firstThree, self.ngramTypes[7])
        return ftFeatures

    def check_belonging(self,x_list,y_list,type):
        ngramFeatures = {}
        for word in x_list:
            if type + '|||' +str(word) in y_list.keys():
                old = ngramFeatures.get(type + '|||' +str(word))
                if old is None:
                    old = 0
                ngramFeatures[type + '|||' + str(word)] = old+1
        return ngramFeatures
    
    def check_belonging_wp(self,x_list,y_list,type):
        ngramFeatures = {}
        
        keys = y_list.keys()
      #  if 'wordpair|||agreed,_agreed' in keys:
       #     print 'yes'
        
        common = Set(keys).intersection(Set(x_list))
        ngramFeatures = dict.fromkeys(common, 1.0)
    #    for c in common:
    #        ngramFeatures[c] = 1.0 # = dict.fromkeys(common, 1.0)
            
        return ngramFeatures
        '''       
        for word in x_list:
            if type + '|||' +str(word) in y_list.keys():
                old = ngramFeatures.get(type + '|||' +str(word))
                if old is None:
                    old = 0
                ngramFeatures[type + '|||' + str(word)] = old+1
        return ngramFeatures
        '''
    
    def getCommon(self,s_arg,t_arg):
        
        PUNCTUATION = (';', ':', ',', '.', '!', '?')

        s_arg_tokens = nltk.word_tokenize(s_arg.lower())
        t_arg_tokens = nltk.word_tokenize(t_arg.lower())
        
        s_arg_tokens_no_periods = [ token for token in s_arg_tokens if token not in  PUNCTUATION] 
        
        
        return len(list(set(s_arg_tokens_no_periods).intersection(t_arg_tokens)))
        
