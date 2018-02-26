from sklearn.datasets import load_svmlight_file
from sklearn import svm, metrics
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import numpy as np


from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV

from sklearn import metrics
from sklearn import cross_validation

import nltk
from random import shuffle


svmPath = "/Users/dg513/work/eclipse-workspace/sarcasm-workspace/sarcasm_dialogue/Corpus/output/svm/"
#trainFile = "pdtb2_ascii_all_0801.txt.linenumbers.multitrain.1125.train.svm"
#trainFile = "pdtb2_ascii_all_0801.txt.linenumbers.expansion.binary.train.1125.train.svm"
#trainFile ="lj_train_all_nowindow_11182014.txt.classification.1125.TRAIN.svm"
#testFile = "lj_test_all_nowindow_11182014.txt.classification.1125.TEST.svm"

trainFile ="tweet.SARCNOSARC.ONLY.CONTEXT.TRAIN.binary.svm.TRAINING.txt"
#testFile = "essay.all.arguments.0617.txt.test.06172015.TEST.svm"

#trainFile = "wd_train_all_nowindow_11182014.txt.classification.posn.new.1125.TRAIN.svm"

#testFile = "lj_test_all_nowindow_10212014.txt.disc.10222014.txt"

def create_embedding_svm_file(vectors,type,vector_length=100):
	
		
	path = '/Users/dg513/work/eclipse-workspace/argument-workspace/JustificationDetection/data/araucaria/input/5folds/'
	folder = 'one'
	file = 'araucaria_claim_premise_check.txt.' + type + folder
	
	f = open(path+folder+'/'+file)

	
	opFile = path + folder + '/' + file +  '.svm'
	writer = open(opFile,'w')
	
	embed_utterances  = []
	categories = []
	f.readline()
	
	#first shuffle the data in some way
	allLines = []
	
	for line in f:
		allLines.append(line)
	f.close()	
	
	shuffle(allLines)
	
	for line in allLines:
	
		category = line.strip().split('\t')[0]
		utterance = line.strip().split('\t')[1]
		
		embed_utterance = word_encode(vector_length, utterance.strip(),vectors)
		embed_utterances.append(embed_utterance)
	#	categories.append(convert(category))
		categories.append(category)


	
	return  np.array(embed_utterances),np.array(categories)
	
def svm_format(embed_encode,length):
		
	embed = str(embed_encode)[1:-1]
	values = embed.split()
	svm = ' '
	for index in range(0,(length)):
		svm += str(index)+':'+str(values[index]) + ' '
		
	svm = svm.strip()
	return svm
	
def convert(label):
	
	if label.strip().lower() == 'sarc':
		return 1.0
	elif label.strip().lower() == 'notsarc':
		return 0.0
	
def word_encode(length, utterance,vectors):
	
	word_list = nltk.word_tokenize(utterance.lower())
	# 
	word_pos_list = nltk.pos_tag(word_list) 
	filtered_words = [word for word in word_list if word not in nltk.corpus.stopwords.words('english') and word.isalpha()]
	embedding_sum = np.zeros(length)
	num = 0.0
	for filtered_word in filtered_words:
		model_embedding = vectors.get(filtered_word.lower())
		if model_embedding is None:
			model_embedding  = np.random.normal(0.0,0.15,length)
			
		num+=1.0
		embedding_sum = np.sum([embedding_sum, model_embedding], axis=0) # vector sum (similar to Mitchell / Lapata but with predicted vectors)
		
	embedding_sum = np.divide(embedding_sum,num) # take the average 

	return embedding_sum
		
	

def crossValidation(vectors):
	X_train, Y_train = create_embedding_svm_file(vectors,'train',vector_length=50)
	
	
	print ('the shape is ' + str(X_train.shape))
	#X_train_new = SelectKBest(chi2, k=30000).fit_transform(X_train, y_train)
	#print ('the shape is ' + str(X_train_new.shape))
#	clf = svm.SVC(kernel='linear', C=1024.0)
#	scores = cross_validation.cross_val_score(clf, X_train, Y_train, cv=5, scoring='f1')

#	print str(scores)
#	target_names = []
	clf = svm.SVC(kernel='linear', C=4.0)
	size = X_train.shape
	k_fold = cross_validation.KFold(size[0], 5)

#	target_names.append("0.0")
#	target_names.append("1.0")
#	target_names.append("2.0")
#	target_names.append("3.0")

	totalP = 0
	totalR = 0
	totalF1 = 0
	for k, (train, test) in enumerate(k_fold):
		clf.fit(X_train[train], Y_train[train])	
		num = 0
		'''	
		for x_train in X_train[test]:
			pred = clf.predict(x_train)
			expected = Y_train[train][num]
		#	print str(pred)
			num = num + 1
	'''
		predict = clf.predict(X_train[test])
		print("Classification report for classifier %s:\n%s\n" % (clf, metrics.classification_report( Y_train[test], predict,digits=4)))
	#	print(metrics.classification_report( Y_train[test],predict) )
	
		
	#	[p, r, f1, s] = metrics.precision_recall_fscore_support(Y_train[test],predict, average=None)
	#	totalP = totalP + p[1]
	#	totalR = totalR + r[1]
	#	totalF1 = totalF1 + f1[1]
		
	#	print("Confusion matrix:\n%s" % metrics.confusion_matrix( Y_train[test], predict) )
	
		#print("[fold {0}]  {1:.5f}, score: {2:.5f}".format(k,  clf.score(X_train[test], Y_train[test])))
	#print  str(totalP/5)   + " " +  str(totalR/5) + " " + str(totalF1/5)
    
def classification(vectors):

	X_train, y_train = create_embedding_svm_file(vectors,'train',vector_length=50)
	
	print ('the shape is ' + str(X_train.shape))
#	X_train_new = SelectKBest(chi2, k=30000).fit_transform(X_train, y_train)
#	print ('the shape is ' + str(X_train_new.shape))
	
	
	X_test, y_test = create_embedding_svm_file(vectors,'test',vector_length=50)# , n_features=30000)#X_train.shape[1])

#training
#svm
	scaler = StandardScaler(with_mean=False)
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.fit_transform(X_test)

	
	clf = svm.SVC(kernel='linear', class_weight='auto')
	#clf = BernoulliNB(alpha=.01)
	#clf = MultinomialNB(alpha=.05)
	
	clf.fit(X_train, y_train)	

	num = 0
	'''
	for x_test in X_test:
		predicted = clf.predict(x_test)
		expected = y_test[num]
		num = num+1
	#	print "number: " + str(num) +   " expected: " + str(expected) + " predicted: " + str(predicted)
	'''
	
	pred = clf.predict(X_test)
	print("Classification report for classifier %s:\n%s\n" % (clf, metrics.classification_report(y_test, pred,digits=4)))
	print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test, pred))

def recursiveFeatSelection():

	X_train, y_train = load_svmlight_file(svmPath + "/" + trainFile)
	X_test, y_test = load_svmlight_file(svmPath + "/" + testFile, n_features=X_train.shape[1])
	
	clf = svm.SVC(kernel='linear', C=1024.0)
	rfecv = RFECV(estimator=clf, step=1, cv=StratifiedKFold(y_train, 2),
              scoring='f1')
	rfecv.fit(X_train, y_train)
	
	print("Optimal number of features : %d" % rfecv.n_features_)


def gridSearch():
	
	X_train, y_train = load_svmlight_file(svmPath + "/" + trainFile)
	X_test, y_test = load_svmlight_file(svmPath + "/" + testFile, n_features=X_train.shape[1])

	
	tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}]#, {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

	#training
#	clf = svm.SVC(kernel='linear')
#	clf.fit(X_features, trainingLabels)	

	scores = ['precision', 'recall']

	for score in scores:
		print("# Tuning hyper-parameters for %s" % score)
		print()

    	clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5, scoring=score)
    	clf.fit(X_train, y_train)
    	print("Best parameters set found on development set:")
    	print()
    	print(clf.best_estimator_)
    	print()
    	print("Grid scores on development set:")
    	print()
    	for params, mean_score, scores in clf.grid_scores_:
    		print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))
    		print()
    		print("Detailed classification report:")
    		print()
    		print("The model is trained on the full development set.")
    		print("The scores are computed on the full evaluation set.")
    		print()
    #	y_true, y_pred = y_test, clf.predict(X_test)
    #	print(classification_report(y_true, y_pred))
    #	print()
    
def loadEmbeddings():
	
	path = '/Users/dg513/work/eclipse-workspace/scratch-workspace/ScratchProject/data/wordnet/glove.6B/'
	file = 'glove.6B.50d.txt'    
	
#	path = '/Users/dg513/work/eclipse-workspace/distrib-workspace/WSDLibSVM/data/config/'
#	file = 'tweet.all.05032015.sg.model.bin.txt'    
	
	
	#V = np.zeros(shape=(len(vocabs),vector_length),dtype=float)
	f = open(path + file, 'r')
  
	num = 0
	
	word_vector = {}
	
	for line in f:
		line = line.strip().lower()
		features = line.split()
		word = features[0]
		word_vector[word]  = np.array(features[1:],dtype="float32")


#		for column, vecVal in enumerate(vector):
#			V[row][column] = float(vecVal)
			#''' normalize weight vector '''
		
	#	V[row] /= math.sqrt((V[row]**2).sum() + 1e-6)
		
#		num+=1

		
	print 'Vectors are read from: '+ file
	f.close()
	
	return word_vector

    
def main():
	
	vectors = loadEmbeddings()
	
#	gridSearch()
#	crossValidation(vectors)
	classification(vectors)
	#recursiveFeatSelection()
main()
	
