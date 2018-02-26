from nltk import bigrams,trigrams
import string
import nltk
from collections import Counter

mainPath = "./auto-grader/ArgumentDetection/"
input = 'data/pdtb/input/'


def listModals(postags, type, dict_x):
    
    counts = Counter(word if 'MD' in tag else None for word,tag in postags )
    for word in counts:
        if word is not None:
            old = dict_x.get(word+'|||'+type)
            if old is None:
                old = 0
            dict_x[type + '|||' +word] = old +counts[word]

def wps(s_arg_tokens,t_arg_tokens):
    
    fv =[]
    for s_arg_token in s_arg_tokens:
        for t_arg_token in t_arg_tokens:
            wp = s_arg_token + '_' + t_arg_token
            fv.append(wp)
    
    return fv

def fthree(arg_tokens,type):
    
    fv = []
    tokens = []
    for i in range(min(3,len(arg_tokens))):
        tokens.append(arg_tokens[i])
        
    fv.append( type +'|||' + '_'.join(tokens) )
    return fv

def firstlast(arg_token,type):
    
    fv = []
    fv.append( type +'|||' + arg_token) 
    return fv

def counts(list_x,dict_x):
    for word in list_x:
        old = dict_x.get(word)
        if old is None:
            old = 0
        dict_x[word] = old +1 
    return dict_x

def write_to_file(file_name,dict_x):
    for word in dict_x:
        file_name.write(str(word)+"\t"+str(dict_x[word])+"\n")

file_type = "alldata"
rel_type = 'contingency'

#wordpairs = open(mainPath + input + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.wp.txt', "w")
#firstthreeFile = open(mainPath + input + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt', "w")
#modalFile = open(mainPath + input + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.modal.txt',"w")
#firstlastFile = open(mainPath + input + 'stab.all.arguments.claim.premise.para.1231.'+ file_type + '.firstlast.txt', "w")
#input_tree = open(mainPath + input + 'stab.all.arguments.claim.premise.para.1231.txt.alldata',"r")



#wordpairs = open(mainPath + input + 'ets.all.arguments.claim.premise.para.1231.'+ file_type + '.wp.txt', "w")
#firstthreeFile = open(mainPath + input + 'ets.all.arguments.claim.premise.para.1231.'+ file_type + '.firstthree.txt', "w")
#firstlastFile = open(mainPath + input + 'ets.all.arguments.claim.premise.para.1231.'+ file_type + '.firstlast.txt', "w")
#modalFile = open(mainPath + input + 'ets.all.arguments.claim.premise.para.1231.'+ file_type + 'modal.txt',"w")                 
#input_tree = open(mainPath + input + 'ets.all.arguments.claim.premise.para.1231.txt.' + file_type,"r")


#wordpairs = open(mainPath + input + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.'+ file_type + '.wp.txt', "w")
#firstthreeFile = open(mainPath + input + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.'+ file_type + '.firstthree.txt', "w")
#firstlastFile = open(mainPath + input + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.'+ file_type + '.firstlast.txt', "w")
#modalFile = open(mainPath + input + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.'+ file_type + 'modal.txt',"w")                 
#input_tree = open(mainPath + input + 'sr_train_all_nowindow_11182014.txt.classification.posn.new.' + file_type,"r")


wordpairs = open(mainPath + input + 'pdtb2_ascii_all_0801.txt.'+ rel_type + '.wp.txt', "w")
firstthreeFile = open(mainPath + input + 'pdtb2_ascii_all_0801.txt.'+ rel_type + '.firstthree.txt', "w")
firstlastFile = open(mainPath + input + 'pdtb2_ascii_all_0801.txt.'+ rel_type + '.firstlast.txt', "w")
modalFile = open(mainPath + input + 'pdtb2_ascii_all_0801.txt.'+ rel_type + 'modal.txt',"w")                 
input_tree = open(mainPath + input + 'pdtb2_ascii_all_0801.txt.' + file_type,"r")


input_tree.readline()
clauses = []
for line in input_tree:
    temp = line.lower().split("\t")
    if temp[2] != 'explicit':
        if temp[4].startswith(rel_type):
            comps = temp[5],temp[6]
            clauses.append(comps)

wp = {}
modals = {}
firstthree = {}
fl = {}

i = 0
for clause in clauses:
 #   print clause
  #  clause = clause.translate(string.maketrans("",""), string.punctuation)
    s_arg = clause[0]
    t_arg = clause[1]
    
    #we have weird use of commas and periods etc. 
    #lets take care of some manually 
    s_arg = s_arg.replace(',',' ')
    t_arg = t_arg.replace(',',' ')
    
    
    s_arg_tokens = nltk.word_tokenize(s_arg)
    t_arg_tokens = nltk.word_tokenize(t_arg)
    
    counts(wps(s_arg_tokens,t_arg_tokens),wp)
    
    counts(fthree(s_arg_tokens,'SOURCE'),firstthree)
    counts(fthree(t_arg_tokens,'TARGET'),firstthree)
    
    counts(firstlast(s_arg_tokens[0],'SOURCE'),fl)
    counts(firstlast(t_arg_tokens[0],'TARGET'),fl)
    
    
    counts(firstlast(s_arg_tokens[-1],'SOURCE'),fl)
    counts(firstlast(t_arg_tokens[-1],'TARGET'),fl)
    
    s_posTags = nltk.pos_tag(s_arg_tokens)
    t_posTags = nltk.pos_tag(t_arg_tokens)

    listModals(s_posTags,'SOURCE',modals)
    listModals(t_posTags,'TARGET',modals)

    i=i+1
    if i % 100 == 0 and i > 0:
        print 'finished ' + str(i) + ' lines'
        
                
write_to_file(wordpairs,wp)
write_to_file(firstthreeFile,firstthree)
write_to_file(modalFile,modals)
write_to_file(firstlastFile,fl)

wordpairs.close()
modalFile.close()
firstthreeFile.close()
firstlastFile.close()

