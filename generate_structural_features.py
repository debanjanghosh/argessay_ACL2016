import nltk
import string

class StructuralFeatures:
    def get_tokens_count(self, sent):
        #Returns float for division in structural features
        #if the sent is only a period - then we do not count!
        if sent in string.punctuation:
            return 0.0 ;
        
        return float(len(nltk.word_tokenize(sent)))

    def get_punctuation_count(self,sent):
        count = 0
        
        #if the sent is only punc we do not count
        if sent in string.punctuation:
            return count
        
        for c in sent:
            if c in string.punctuation:
                count += 1
        return count
