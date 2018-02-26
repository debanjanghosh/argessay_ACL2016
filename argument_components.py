from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures
from generate_structural_features import StructuralFeatures

import ConfigParser


from sets import Set
import datetime

'''
    This class is the main interface for generating features for argument components.
    The output are SVM/Weka files
    Written by Debanjan and Aquila
    Caution: very low comments/documentation
'''

class EssayClassifier:
    
    def __init__(self):
        
        self.features_list = []
        self.selected = []

        print 'init done'

    def setInitExperiment(self):
        
        #setting the objects for different feature types
        #structural, syntactic, lexical, indicators (see SG2014 for more details)
        #we set the objects as well as some files for training processing
        
        if 'struct' in self.feature_types :
            self.structFeat = StructuralFeatures()
            
        if 'syn' in self.feature_types :
            self.synFeat = SyntacticFeatures()
            #for training or test - we use the "prodTreeTrainFile" 
            #since we don't want to add new production rules to the training process
            productionFile = self.mainPath + self.input_path + self.prodTreeTrainFile
            self.synFeat.setProductionFile(productionFile)
            
        if 'lex' in self.feature_types :    
            self.lexFeat = LexicalFeatures()
            unigramFile = self.mainPath + self.input_path + self.unigram_file
            bigramFile = self.mainPath + self.input_path + self.bigram_file
            trigramFile = self.mainPath + self.input_path + self.trigram_file
            verbs = self.mainPath + self.input_path + self.verb_file
            adverbs = self.mainPath +self.input_path + self.adverb_file
            modals = self.mainPath + self.input_path + self.modal_file
            self.lexFeat.setFileNames(unigramFile,bigramFile,trigramFile,verbs,adverbs,modals)
                
        if 'ind' in  self.feature_types :    
            self.indicatorFeat = IndicatorFeatures()
            discourseMarkerFile = self.mainPath + self.input_path + self.discourse_marker_file
            self.indicatorFeat.setDiscourseMarkers(discourseMarkerFile)

        print 'initialization done'
    
    def loadParams(self):

        #input parameters are in the argcomp.ini file
        #feel free to change the parameters as needed
        fileName = 'argcomp.ini'
        
        config = ConfigParser.ConfigParser()
        config.read('./auto-grader/ArgumentDetection/data/config/' + fileName)
        
        self.file_type = config.get('section1', 'file_type') 
        self.expr_type = config.get('section1', 'expr_type') 
        
        self.mainPath = config.get('section1', 'mainPath')
        self.input_path = config.get('section1', 'input_path')
        self.output_path = config.get('section1', 'output_path')

        
        self.constTreeTrainFile = config.get('section1','constTreeTrainFile')
        self.constTreeTestFile = config.get('section1','constTreeTestFile')

        self.prodTreeTrainFile = config.get('section1','prodTreeTrainFile')
        self.prodTreeTestFile = config.get('section1','prodTreeTestFile')

        self.inputSentTrainFile = config.get('section1','inputSentTrainFile')
        self.inputSentTestFile = config.get('section1','inputSentTestFile')

        self.deptreeTrainFile = config.get('section1','deptreeTrainFile')
        self.deptreeTestFile = config.get('section1','deptreeTestFile')

        
        self.unigram_file = config.get('section1','unigram_file')
        self.bigram_file = config.get('section1','bigram_file')
        self.trigram_file = config.get('section1','trigram_file')
        self.verb_file = config.get('section1','verb_file')
        self.adverb_file = config.get('section1','adverb_file')
        self.modal_file = config.get('section1','modal_file')
        self.discourse_marker_file = config.get('section1','discourse_marker_file')

        self.feature_types = config.get('section2', 'feature_types').split(',')
        

    #def read_files(self, file_type, mainPath,input,output):
    def read_files(self):

        #read the input files 
        #separate files for training and test purpose 
        if self.expr_type == 'train':
            input_tree = open(self.mainPath + self.input_path + self.constTreeTrainFile,"r")
            input_sent = open(self.mainPath + self.input_path + self.inputSentTrainFile,"r")
            input_production_tree = open(self.mainPath + self.input_path +self.prodTreeTrainFile,"r")
            input_dep_tree = open(self.mainPath + self.input_path +self.deptreeTrainFile,"r")
                
        if self.expr_type == 'test':
         #these are ETS files 
                input_tree = open(self.mainPath + self.input_path + self.constTreeTestFile,"r")
                input_sent = open(self.mainPath + self.input_path + self.inputSentTestFile,"r")
                input_production_tree = open(self.mainPath + self.input_path +self.prodTreeTestFile,"r")
                input_dep_tree = open(self.mainPath + self.input_path +self.deptreeTestFile,"r")
     
        print 'input files are loaded...'

        if self.expr_type == 'train':
            self.output_file = open(self.mainPath + self.output_path +"svm/features_"+self.file_type + '_' + self.expr_type + '.0324.' + 
                                str(self.feature_types) +'.svm',"w")
            self.weka_output_file = open(self.mainPath + self.output_path + "weka/features_weka"+self.file_type + '_' + self.expr_type + '.0324.'+
                                             str(self.feature_types)+ '.arff',"w")
           
        if self.expr_type == 'test':
            self.output_file = open(self.mainPath + self.output_path +"svm/features_"+self.file_type + '_' + self.expr_type + '.0324.' +
                                str(self.feature_types) + '.svm',"w")
            self.weka_output_file = open(self.mainPath + self.output_path + "weka/features_weka"+self.file_type + '_' + self.expr_type +'.0324.' +str(self.feature_types) +'.arff',"w")
                 
        self.names = open(self.mainPath + self.output_path +"feature_names","w")
        
        self.labels = Set()

        argument = []
        input_tree.readline()
        clauses = []
        for line in input_tree:
            temp = line.split("\t")
            clauses.append(temp[2].lower()) 
            argument.append(temp[1].lower()) 
            self.labels.add(temp[1].lower()) 

        self.clauses = clauses
        self.argument = argument

        input_sent.readline()
        sents = []
        self.fileIds = []
        for line in input_sent:
            temp = line.lower().split("\t")
            sents.append([temp[2],temp[3],temp[4],temp[5],temp[7],temp[8]]) 
            self.fileIds.append([temp[0],temp[6]])

        self.sents = sents

        input_production_tree.readline() #header
        self.sent_production_trees = []
        for line in input_production_tree:
            self.sent_production_trees.append(line.split("\t")[2][1:-2])#.strip().split(",")) #3 for stab

        input_dep_tree.readline() # header
        self.sent_deep_trees =[]
        for line in input_dep_tree:
            self.sent_deep_trees.append(line.split("\t")[2])#.strip().split(",")) #3 for stab

        
    def populate_features(self):

        #populating all the features
        if len(self.clauses) != len(self.sents):
            print "Error: consttree and file do not match"
            exit()
            
        #weka write the header
        # structural features
        featureNames = ["ARG_TOKENS","COVERING_TOKENS","TOKEN_RATIO","TOKEN_STAT","PRECEDING_TOKENS","FOLLOWING_TOKENS","INTRO_POS","CONCL_POS", "INTRO_PARA", "CONCL_PARA","FIRST_PARA", "LAST_PARA","COVERING_POS","ARG_PUNCT","COVERING_PUNCT","PRECEDING_PUNCT","FOLLOWING_PUNCT","QUESTION"]
        self.features_list.extend(featureNames)
        #syntactic features
        featureNames = ["SUB-CLAUSES","DEPTH","PRESENT_TENSE"]
        self.features_list.extend(featureNames)
        #lexical features
        featureNames = ["MODALS"]
        self.features_list.extend(featureNames)
 #    discourse features
        featureNames = ["FIRST_PERSON"]
        self.features_list.extend(featureNames) 
        
        #update with all feature names!!!
        #here I will be getting the lexical features
        #NOTE: depending upon the DF value this will result in a dynamic list
        self.getAllFeatureNames()
 
        #write the prologue/beginning of the weka file 
        self.writePrologueWeka()
        self.weka_output_file.write('\n')
        self.weka_output_file.write("@data")
        self.weka_output_file.write('\n')
    
        print 'weka initialization done'

        THRESHOLD = 5
        for i in range(len(self.clauses)):
            self.features = {}
            clause = self.clauses[i]
            sent = self.sents[i]
            arg = self.argument[i]
            production = self.sent_production_trees[i]
            deptrees = self.sent_deep_trees[i]
            fileId = self.fileIds[i]
            
            if len(sent[0]) < THRESHOLD: #length of argument
                continue 


            if 'struct' in self.feature_types :
                self.structural_features(sent)
        
            if 'syn' in self.feature_types :
                self.syntactic_features(clause,production,deptrees)

            if 'lex' in self.feature_types :    
                self.lexical_features(sent)
                
            if 'ind' in  self.feature_types :    
                self.indicator_features(sent)
            
          #  self.output_file.write(str(arg)+"\t")
           # print sent[0]
            wekaString, svmString = self.createWekaSVMString(str(arg),fileId)
            self.weka_output_file.write(wekaString)
            self.output_file.write(svmString)
            self.weka_output_file.write('\n')
            self.output_file.write("\n")
            
            if i % 100 == 0 and i > 0:
                print 'finished ' + str(i) + ' lines'
                
           
        self.output_file.close()
        self.weka_output_file.close()

        for i in range(len(self.features_list)):
            self.names.write(str(i)+":"+str(self.features_list[i])+"\n")
        self.names.close()     
    def structural_features(self,sent):
        #sent = (argument component, covering sentence)
        # get_tokens_count() returns float
        
        arg = sent[0]
        sentence = sent[1]
        lineNum = sent[2]
        totalLine = sent[3]
        paragraph = sent[4]
        totalPara = sent[5]
        
    #    print arg, ' ', sentence
        
        self.features["ARG_TOKENS"] = self.structFeat.get_tokens_count(arg)
        self.features["COVERING_TOKENS"] = self.structFeat.get_tokens_count(sentence)
        #number of tokens preceding and following an argument component in the covering sentence
        if self.features["ARG_TOKENS"] == 0.0 :
             self.features["TOKEN_RATIO"] = 0.0;
        else :    
            self.features["TOKEN_RATIO"] = self.features["COVERING_TOKENS"]/self.features["ARG_TOKENS"]
            
        if self.features["ARG_TOKENS"] == self.features["COVERING_TOKENS"]:
            self.features["TOKEN_STAT"] = 1
        else:
            index = sentence.find(arg)
            if index != -1:
                preceding_sent = sentence[:index]
                following_sent = sentence[index+len(arg):]
                self.features["PRECEDING_TOKENS"] = self.structFeat.get_tokens_count(preceding_sent)
                self.features["PRECEDING_PUNCT"] = self.structFeat.get_punctuation_count(preceding_sent)
                self.features["FOLLOWING_TOKENS"] = self.structFeat.get_tokens_count(following_sent)
                self.features["FOLLOWING_PUNCT"] = self.structFeat.get_punctuation_count(following_sent)
       
       #line position before paragraph features         
        if self.occursInBegin(int(lineNum),int(totalLine ) ) == True:
            self.features["INTRO_POS"] = 1
            
        if self.occursInEnd(int(lineNum),int(totalLine) ) == True:
            self.features["CONCL_POS"] = 1
        
        if int(paragraph) == 0:
            self.features["INTRO_PARA"] = 1
        if int(paragraph) >= int(totalPara)-1:
            self.features["CONCL_PARA"] = 1
        
        if int(lineNum) == 0:
            self.features["FIRST_PARA"] = 1
        if int(lineNum) >= int(totalLine)-1 :
            self.features["LAST_PARA"]  = 1
     
     
        self.features["COVERING_POS"] = lineNum
        self.features["ARG_PUNCT"] = self.structFeat.get_punctuation_count(arg)
        self.features["COVERING_PUNCT"] = self.structFeat.get_punctuation_count(sentence)
        if sentence.strip()[-1] == "?":
            self.features["QUESTION"] = 1
     
    def occursInBegin(self, sentPos, allSentPos):
        perc_20 = float(allSentPos) * 0.2
        if sentPos <= perc_20:
            return True
        else:
            return False
        
    def occursInEnd(self,sentPos, allSentPos):
        perc_80 = float(allSentPos) * 0.8
        if sentPos >= perc_80:
            return True
        else:
            return False
         
    def syntactic_features(self,clause,production,deptree):
        #Syntactic Features

        self.features["SUB-CLAUSES"] = self.synFeat.get_subclauses(clause)
        self.features["DEPTH"] = self.synFeat.get_depth(clause)
        self.features["PRESENT_TENSE"] = self.synFeat.is_present_tense(clause,deptree)
        productionFeatures = self.synFeat.get_productions(production)
        self.features.update(productionFeatures)

    def lexical_features(self,sent):
        #Lexical Features
        #binary feature
        modalFeatures = self.lexFeat.get_modals(sent[0])
        self.features.update(modalFeatures)
        if modalFeatures:
            self.features["MODALS"] = "1"
        #binary for each verb-
        
       # self.features["VERBS"] = lexFeat.get_verbs(clause) //original
        verbFeatures = self.lexFeat.get_verbs(sent[0])
        self.features.update(verbFeatures) 

        adverbFeatures = self.lexFeat.get_adverbs(sent[0])
        self.features.update(adverbFeatures)
         
        ngramFeatures = self.lexFeat.get_ngrams(sent[1])
        self.features.update(ngramFeatures)

    def indicator_features(self,sent):
        #Indicator Features
        discourseFeatures= self.indicatorFeat.get_discourse_marker(sent[0],sent[1])
        self.features.update(discourseFeatures)
        firstPersons = self.indicatorFeat.get_first_person(sent[1])
        if firstPersons:
            self.features["FIRST_PERSON"] = 1

    def loadTopFeatures(self):
       # file = open(self.mainPath + self.stabInput + "top_features_0617.txt")
        file = open(self.mainPath + './data/config/' + "top_features_ets_1000_1231.txt")

        line = file.readline()
        line = line[1:len(line)-1]
        features = line.split(',')
        for feature in features:
          #  print feature
            self.selected.append(int(feature.strip()))
    #    self.selected = [ int(feature.strip()) for feature in line.split(',')]
        #sorted_list = sorted(self.selected)
        file.close()
        
    def createWekaSVMString(self, arg, fileId):
        fileIdStr = '#' + fileId[0] + '_' + fileId[1]
        fileIdStr = fileIdStr.strip()
        
        wekaBuffer = '{ ' 
        svmBuffer = arg + ' '
        for i in range(len(self.features_list)):
               
                key = self.features_list[i]
                value = self.features.get(key)
                
                if self.selected:
                    if i not in self.selected:
                        value = 0
                
                if value is not None and value > 0 :
                    wekaBuffer = wekaBuffer  + str(i) + ' ' + str(value) + ',' + ' '
                    svmBuffer = svmBuffer + str(i+1) + ':' + str(value) + ' '
                    
        wekaBuffer = wekaBuffer  + str(len(self.features_list)) + ' ' + arg + '}'
        svmBuffer = svmBuffer + ' ' + fileIdStr
        svmBuffer = svmBuffer.strip()
        return wekaBuffer, svmBuffer
          
    def getAllFeatureNames(self):
        
   #     nonNGramFeatSize = len(self.features_list)
       
        if 'lex' in self.feature_types :    
            self.features_list.extend(self.lexFeat.getVerbFeats())
            self.features_list.extend(self.lexFeat.getAdverbFeats())
            self.features_list.extend(self.lexFeat.getUnigramFeats())
            self.features_list.extend(self.lexFeat.getBigramFeats())
            self.features_list.extend(self.lexFeat.getTrigramFeats())
            self.features_list.extend(self.lexFeat.getModals()) 
            
        if 'syn' in self.feature_types :
            self.features_list.extend(self.synFeat.getProductionFeats())
        
        if 'ind' in  self.feature_types :    
            self.features_list.extend(self.indicatorFeat.getDiscourseFeats())
            self.features_list.extend(self.indicatorFeat.getFirstPersonFeats())

                                          
    def writePrologueWeka(self):
        
        self.weka_output_file.write("% Weka ARFF file")
        self.weka_output_file.write('\n')
        self.weka_output_file.write("% Generated by Python Program: argument component")
        self.weka_output_file.write('\n')
        self.weka_output_file.write("% " + str(datetime.datetime.now().time()))
        self.weka_output_file.write('\n')
        self.weka_output_file.write("@RELATION arguments") 
        self.weka_output_file.write('\n')
        
        size = len(self.features_list)
        for index in range(0,size):
            #if index not in self.selected:
             #   continue
            #@ATTRIBUTE 1                              NUMERIC
            att = self.features_list[index] 
            att =att.replace("'", "-")
            #self.weka_output_file.write("@ATTRIBUTE" + " " + "\"" + att +"\"" +  " " + "NUMERIC")
            self.weka_output_file.write("@ATTRIBUTE" + " "  + str(index)  +  " " + "NUMERIC")

            self.weka_output_file.write('\n')
        
        #@ATTRIBUTE '-label-'                      {sarcasm,negative,positive}
        label = self.createStringOnLabels()
        self.weka_output_file.write("@ATTRIBUTE '-label-' " + label) 
        
    
    def createStringOnLabels(self):
        return '{' + ','.join(self.labels) + '}'
    

e = EssayClassifier()
e.loadParams()
e.setInitExperiment()
e.read_files()
        #e.loadTopFeatures()
        #e.loadParameters()
e.populate_features()
    
#    if __name__ == '__main__':
 #       main()

