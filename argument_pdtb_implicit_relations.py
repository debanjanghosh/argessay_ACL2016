from generate_syntactic_features import SyntacticFeatures
from generate_lexical_features import LexicalFeatures
from generate_indicator_features import IndicatorFeatures
from generate_structural_features import StructuralFeatures
from decorator import init

from sets import Set
import datetime

#this is for implicit relation identification 
#similar code as argument_relations.py but this script will be used 
#for justification/stance/rational experiments....

class ArgumentPair:
    
    def __init__(self):
        
        #   file_type = "train"
        self.file_type = "test"
        self.file_type = "alldata"
     #   self.file_type = "ets"
     
        self.pdtb_type = 'explicit'
      	
        self.pdtb_rel = 'comparison'
        
        self.technoInput = 'data/technorati/input/'

        
        self.expr_type = 'train'
   #     self.expr_type = 'test'
      
   #     loadParams(self)
        self.selected = []
        
        self.mainPath = "./auto-grader/ArgumentDetection/"
        
        self.pdtbInput = 'data/pdtb/input/'
        self.pdtbOutput = 'data/pdtb/output/'
        
        self.feature_types = ['struct']
     #   self.feature_types = ['syn']
     #   self.feature_types = ['lex']
      #  self.feature_types = ['ind']
     #   self.feature_types = ['pred']
       
                               
        self.feature_types = ['struct','syn','lex','ind']#,'pred']
        self.features_list = []
        
        #self.read_files(self.file_type,self.mainPath)
        self.pdtb_read_files(self.file_type,self.mainPath)

        
        
        if 'struct' in self.feature_types :
            self.structFeat = StructuralFeatures()
        if 'syn' in self.feature_types :
            self.synFeat = SyntacticFeatures()
           # productionFile = self.mainPath + self.pdtbInput + 'pdtb2_ascii_all_0801.txt.07302016.consttree.productions'
            productionFile = self.mainPath + self.pdtbInput + 'but_positive.csv.consttree.productions'

            self.synFeat.setPDTBRelationProductionFile(productionFile,self.pdtb_rel)
         #   self.synFeat.setTargetProductionFile(self.input_target_production)
        if 'lex' in self.feature_types :    
            self.lexFeat = LexicalFeatures()
            modals = self.mainPath + self.technoInput + "modals_all_1231.txt"
            self.lexFeat.setModalFile(modals)
       #     self.lexFeat.setArgRelationWordPairFile(self.mainPath + self.pdtbInput + "pdtb2_ascii_all_0801.txt." + 
       #                                             self.pdtb_rel + ".wp.txt")
            self.lexFeat.setFirstThreeFile(self.mainPath + self.pdtbInput + 'pdtb2_ascii_all_0801.txt.'+ self.pdtb_rel +  '.firstthree.txt')
            self.lexFeat.setFirstLast(self.mainPath + self.pdtbInput + 'pdtb2_ascii_all_0801.txt.' +  self.pdtb_rel  +'.firstlast.txt')
      
        if 'ind' in  self.feature_types :    
            self.indicatorFeat = IndicatorFeatures()
            discourseMarkerFile = self.mainPath + self.technoInput + 'pdtb2_unique_lc_markers_notempo_0801.txt'
            self.indicatorFeat.setDiscourseMarkers(discourseMarkerFile)

            
    def read_files(self, file_type, mainPath):
        
        #stab
        if self.expr_type == 'train':
                inputFile = mainPath + self.technoInput + "sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata." + self.expr_type
                self.input_sent = open(inputFile,"r")
                print 'reading the inputFile: ' + inputFile
           #     self.input_wp = mainPath + self.stabInput + "stab.all.arguments.claim.premise.para.1231." + file_type + ".wp.txt"
           #     self.input_ft = mainPath + self.stabInput + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt'
         
                self.input_consttree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.consttree', "r" )
                self.input_deptree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.deptree', "r" ) 
                self.input_production_tree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.consttree.productions', "r")

        if self.expr_type == 'crossval':
                inputFile = mainPath + self.technoInput + "sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata" 
                self.input_sent = open(inputFile,"r")
                print 'reading the inputFile: ' + inputFile
           #     self.input_wp = mainPath + self.stabInput + "stab.all.arguments.claim.premise.para.1231." + file_type + ".wp.txt"
           #     self.input_ft = mainPath + self.stabInput + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt'
         
                self.input_consttree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata' + '.consttree', "r" )
                self.input_deptree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata'+  '.deptree', "r" ) 
                self.input_production_tree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+  'consttree.productions', "r")


        if self.expr_type == 'test':
                inputFile = mainPath + self.technoInput + "sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata." +self.expr_type
                self.input_sent = open(mainPath + self.technoInput + "sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata." +self.expr_type,"r")
         
                print 'reading the inputFile: ' + inputFile
            #    self.input_wp = open(mainPath + self.etsInput + "ets.all.arguments.claim.premise.para.1231." + file_type + ".wp.txt", "r")
             #   self.input_ft = open(mainPath + self.etsInput + 'ets.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt', "r")
                
                self.input_consttree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.consttree', "r" )
                self.input_deptree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.deptree', "r" ) 
                self.input_production_tree = open(mainPath + self.technoInput + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata.'+ self.expr_type + '.consttree.productions', "r")

            #ets files

        if self.expr_type == 'train':
                 self.svm_output_file = open(self.mainPath + self.technoOutput +"svm/argument_relations_features_"+self.expr_type + '.1231.' + 
                                str(self.feature_types) +'.svm',"w")
                 self.weka_output_file = open(self.mainPath + self.technoOutput + "weka/argument_relations_features_weka"+self.expr_type + '.1231.'+
                                     str(self.feature_types)+ '.arff',"w")
        if self.expr_type == 'crossval':
                 self.svm_output_file = open(self.mainPath + self.technoOutput +"svm/argument_relations_features_"+self.expr_type + '.1231.' + 
                                str(self.feature_types) +'.svm',"w")
                 self.weka_output_file = open(self.mainPath + self.technoOutput + "weka/argument_relations_features_weka"+self.expr_type + '.1231.'+
                                     str(self.feature_types)+ '.arff',"w")
     
       
        
        if self.expr_type == 'test':
                self.svm_output_file = open(self.mainPath + self.technoOutput +"svm/argument_relations_features_"+self.file_type + '_' + self.expr_type + '.1231.' +
                                str(self.feature_types) + '.svm',"w")
                self.weka_output_file = open(self.mainPath + self.technoOutput + "weka/argument_relations_features_weka"+self.file_type + '_' + self.expr_type +'.1231.' +str(self.feature_types) +'.arff',"w")
     
     
        
        self.names = open(mainPath + "data/arg_rel_feature_names","w")

        #read the input file 
        self.labels = Set()
        self.input_sent.readline() #header 
        self.sents = []
        for line in self.input_sent:
            self.sents.append(line.split("\t"))
            self.labels.add(line.split("\t")[0])
            
        #we will load the other files here ---    
        
        #load production file 
        self.input_production_tree.readline() #header
        self.sent_production_trees = []
        for line in self.input_production_tree:
            production_tree = line.split("\t")[3][1:-2],line.split("\t")[4][1:-2] # check the tabs 
            self.sent_production_trees.append(production_tree)

    def pdtb_read_files(self, file_type, mainPath):
        
        #stab
        if self.expr_type == 'train':
                inputFile = mainPath + self.pdtbInput + "pdtb2_ascii_all_0801.txt.alldata"
                inputFile = mainPath + self.pdtbInput + "but_positive.csv"
                
                self.input_sent = open(inputFile,"r")
                print 'reading the inputFile: ' + inputFile
           #     self.input_wp = mainPath + self.stabInput + "stab.all.arguments.claim.premise.para.1231." + file_type + ".wp.txt"
           #     self.input_ft = mainPath + self.stabInput + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt'
         
                self.input_consttree = open(mainPath + self.pdtbInput + 'pdtb2_ascii_all_0801.txt.07302016' + '.consttree', "r" )
                self.input_consttree = open(mainPath + self.pdtbInput + 'but_positive.csv' + '.consttree', "r" )

           #     self.input_deptree = open(mainPath + self.pdtbInput + ''+ self.expr_type + '.deptree', "r" ) 
               # self.input_production_tree = open(mainPath + self.pdtbInput + 'pdtb2_ascii_all_0801.txt.07302016.consttree.productions', "r")
                self.input_production_tree = open(mainPath + self.pdtbInput + 'but_positive.csv.consttree.productions', "r")

       
        if self.expr_type == 'train':
                 self.svm_output_file = open(self.mainPath + self.pdtbOutput +"svm/but_positive_argument_relations_features_"+self.pdtb_rel + '.1231.' + 
                                str(self.feature_types) +'.svm',"w")
                 self.weka_output_file = open(self.mainPath + self.pdtbOutput + "weka/but_postivie_argument_relations_features_weka"+self.pdtb_rel + '.1231.'+
                                     str(self.feature_types)+ '.arff',"w")
         
        self.names = open(mainPath + "data/arg_rel_feature_names","w")

        #read the input file 
        self.labels = Set()
        self.input_sent.readline() #header 
        self.sents = []
        for line in self.input_sent:
            features = line.split(',')
            if len(features) <4:
                continue
       #     if features[2].lower() != self.pdtb_type:
        #        continue
         #   if features[2].lower() == 'altlex':
          #      continue 
            check = 'comparison'
            relation = 'comparison' #features[4]
            self.pdtb_rel = relation
            if check.lower().startswith(self.pdtb_rel):
                self.labels.add("1")
                args = "1",relation,features[2],features[3]
                self.sents.append(args)
            else:
                self.labels.add("0")
                args = "0",relation,features[2],features[3]
                self.sents.append(args)

                
        #we will load the other files here ---    
        
        #load production file 
        self.input_production_tree.readline() #header
        self.sent_production_trees = []
        for line in self.input_production_tree:
            features = line.split("\t")
        #    if features[2].lower() != self.pdtb_rel:
        #        continue 
            
            production_tree = line.split("\t")[3][1:-2],line.split("\t")[4][1:-2] # check the tabs 
         #   production_tree = line.split("\t")[1][1:-2],line.split("\t")[2][1:-2] # check the tabs 
            
            self.sent_production_trees.append(production_tree)

            
    def populate_features(self):
        
        self.features_list = [ "S_TOKENS", "T_TOKENS", "TOKEN_DIFFERENCE", "S_PUNCS","T_PUNCS" ,
                              "PUNC_DIFFERENCE", "S_POSITION", "T_POSITION","S_POSN_INTRO", "S_POSN_CONCL", 
                                "T_BEFORE_S", "SENT_DIST", "SAME_SENT","COMMON_PRODS" ] #Structural Features
        
        featureNames = ["SUB-CLAUSES","DEPTH","PRESENT_TENSE"]
        self.features_list.extend(featureNames)
     
        
        featureNames = ["S_MODALS","T_MODALS"]
        self.features_list.extend(featureNames)
        
        featureNames = ["COMMON_TOKENS"]
        self.features_list.extend(featureNames)
        
        featureNames = ["S_ARGTYPE","T_ARGTYPE"]
        self.features_list.extend(featureNames)
        
        
         #update with all feature names!!!
        self.getAllFeatureNames()
 
        #write the prologue/beginning of the weka file 
        self.writePrologueWeka()
        self.weka_output_file.write('\n')
        self.weka_output_file.write("@data")
        self.weka_output_file.write('\n')
    
        print 'weka initialization done'
        
        
        THRESHOLD = 5 #Lexical feature}   
        for i in range(len(self.sents)):
            
            sent = self.sents[i]
            self.features = {}
            label = sent[0]
            relation = sent[1]
            source_arg = sent[2]
            target_arg = sent[3]
            
            source_arg = source_arg.replace(',',' ')
            target_arg = target_arg.replace(',',' ')
   
            
            s_production, t_production = self.sent_production_trees[i]
      
            
            if len(source_arg) < THRESHOLD:
                continue 

            if 'struct' in self.feature_types :
                self.structural_features(source_arg,target_arg)
            
            if 'lex' in self.feature_types:
                self.lexical_features(source_arg,target_arg)
                #self.wordpair_features(source_arg,target_arg)
            
            if 'syn' in self.feature_types:
                self.syntactic_features(s_production, t_production)
                
            if 'ind' in self.feature_types:
                self.indicator_features(source_arg, target_arg)
            
           # if 'pred' in self.feature_types:
           #     self.predicted_features(source_arg_type, target_arg_type)
            
            
            wekaString, svmString = self.createWekaSVMString(self.binaryConvert(str(label)),relation,None)
            self.weka_output_file.write(wekaString)
            self.svm_output_file.write(svmString)
            self.weka_output_file.write('\n')
            self.svm_output_file.write("\n")
            
            if i % 100 == 0 and i > 0:
                print 'finished ' + str(i) + ' lines'
           # if i == 10000:
           #     break
           
        self.svm_output_file.close()
        self.weka_output_file.close()

        for i in range(len(self.features_list)):
            self.names.write(str(i)+":"+str(self.features_list[i])+"\n")
        self.names.close()     
    
    def binaryConvert(self,label):
        
        if int(label) == 1:
            return "1" 
        else:
            return "0"
    
    def writePrologueWeka(self):
        
        self.weka_output_file.write("% Weka ARFF file")
        self.weka_output_file.write('\n')
        self.weka_output_file.write("% Generated by Python Program: argument relations")
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
        
        #only binary 
        self.labels = {"0", "1"}
        return '{' + ','.join(self.labels) + '}'

    
    
    def getAllFeatureNames(self):
        
   #     nonNGramFeatSize = len(self.features_list)
       
        if 'lex' in self.feature_types :    
      #      self.features_list.extend(self.lexFeat.getWordPairFeats())
            self.features_list.extend(self.lexFeat.getFirstThirdFeats())
            self.features_list.extend(self.lexFeat.getFirstLastFeats())
          #  self.features_list.extend(self.lexFeat.getModals()) 
            
        if 'syn' in self.feature_types :
            self.features_list.extend(self.synFeat.getSourceProductionFeats())
          #  self.features_list.extend(self.synFeat.getTargetProductionFeats())

        if 'ind' in  self.feature_types :    
            self.features_list.extend(self.indicatorFeat.getSourceDiscourseFeats())
            self.features_list.extend(self.indicatorFeat.getTargetDiscourseFeats())


    def wordpair_features(self,source_arg,target_arg):
        
        wordPairs = self.lexFeat.createWordPairs(source_arg,target_arg)
        self.features.update(wordPairs)
    
    def lexical_features(self,source_arg,target_arg):
        
    #    wordPairs = self.lexFeat.createWordPairs(source_arg,target_arg)
    #    self.features.update(wordPairs)
        
      #  if wordPairs:
       #     print 'here'
        
   #     print 'wp features are ready'
        
        firstThirdWords = self.lexFeat.createFirstThirdWords(source_arg,target_arg)
        self.features.update(firstThirdWords)
        
   #     print 'firstthird features are ready'

        
        firstLastWords = self.lexFeat.createImplicitFirstLastWords(source_arg,target_arg)
        self.features.update(firstLastWords)
        
    #    print 'firstlast features are ready'

        
        
        modalFeatures = self.lexFeat.get_modals(source_arg)
        if modalFeatures:
            self.features["S_MODALS"] = "1"
        modalFeatures = self.lexFeat.get_modals(target_arg)
        if modalFeatures:
            self.features["T_MODALS"] = "1"
        
        common =self.lexFeat.getCommon(source_arg,target_arg)
        self.features["COMMON_TOKENS"] = common
        
    def syntactic_features(self,s_production,t_production):
        
        productionFeatures1 = self.synFeat.get_rel_productions(s_production,'SOURCE')
        self.features.update(productionFeatures1)

        productionFeatures2 = self.synFeat.get_rel_productions(t_production,'TARGET')
        self.features.update(productionFeatures2)
        
        productionFeatures1Set = set(productionFeatures1)
        productionFeatures2Set = set(productionFeatures2)
        
        commonFeatures = productionFeatures1Set.intersection(productionFeatures2Set)
        self.features["COMMON_PRODS"] =len(commonFeatures)
        

    def indicator_features(self,source_arg,target_arg):
        #Indicator Features
        discourseFeatures1 = self.indicatorFeat.get_implicit_type_discourse_marker(source_arg,'SOURCE')
        self.features.update(discourseFeatures1)

        discourseFeatures2 = self.indicatorFeat.get_implicit_type_discourse_marker(target_arg,'TARGET')
        self.features.update(discourseFeatures2)
        
    def predicted_features(self,s_type,t_type):
     
        self.features["S_ARGTYPE"] = s_type
        self.features["T_ARGTYPE"] = t_type
    
    def loadTopFeatures(self):
       # file = open(self.mainPath + self.stabInput + "top_features_0617.txt")
        file = open(self.mainPath + './data/config/' + "top_features_stab_100_reln_1231.txt")

        line = file.readline()
        line = line[1:len(line)-1]
        features = line.split(',')
        for feature in features:
          #  print feature
            self.selected.append(int(feature.strip()))
    #    self.selected = [ int(feature.strip()) for feature in line.split(',')]
        #sorted_list = sorted(self.selected)
        file.close()
        
    def createWekaSVMString(self, arg, relation=None,fileId=None):
        if fileId is None:
            fileIdStr = '#' + relation
        else:
            fileIdStr = '#' + fileId[0] + '_' + fileId[1]
            fileIdStr = fileIdStr.strip()
        
        wekaBuffer = '{ ' 
        svmBuffer = arg + ' '
        for i in range(len(self.features_list)):
               
                key = self.features_list[i]
                value = self.features.get(key)
                
            #    if self.selected:
            #        if i not in self.selected:
            #            value = 0
                
                if value is not None and value > 0 :
                    wekaBuffer = wekaBuffer  + str(i) + ' ' + str(value) + ',' + ' '
                    svmBuffer = svmBuffer + str(i+1) + ':' + str(value) + ' '
                    
        wekaBuffer = wekaBuffer  + str(len(self.features_list)) + ' ' + arg + '}'
        svmBuffer = svmBuffer + ' ' + fileIdStr
        svmBuffer = svmBuffer.strip()
        return wekaBuffer, svmBuffer


    def structural_features(self,source_arg,target_arg ):
        
        #Structural Features
        self.features["S_TOKENS"] = self.structFeat.get_tokens_count(source_arg)
        self.features["T_TOKENS"] = self.structFeat.get_tokens_count(target_arg)
        self.features["TOKEN_DIFFERENCE"] = abs(self.features["S_TOKENS"] - self.features["T_TOKENS"])

        self.features["S_PUNCS"] = self.structFeat.get_punctuation_count(source_arg)
        self.features["T_PUNCS"] = self.structFeat.get_punctuation_count(target_arg)
        self.features["PUNC_DIFFERENCE"] = abs(self.features["S_PUNCS"] - self.features["T_PUNCS"])


r = ArgumentPair()
#r.loadTopFeatures()
r.populate_features()
