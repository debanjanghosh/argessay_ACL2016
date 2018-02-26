
total_f1 = 0

def baselineHeuristic(input,ip):
    
    f1 = open(input+ip)
    f1.readline()
    lines = f1.readlines()
    golds = [ line.split()[0] for line in lines]
    f1.close()
    
    stancePosns = [line.split('\t')[3] for line in lines ]
    rationalesPosns = [line.split('\t')[4] for line in lines ]
    
    preds = []
    
   # preds = [ int(rationale) - int(stance) for stance in stancePosns and rationale in rationalesPosns]
    
    for index in range(len(stancePosns)):
        stance = stancePosns[index]
        rationale = rationalesPosns[index]
        if int(rationale) - int(stance) == 1:
            preds.append(1)
        else:
            preds.append(0) 
    
    
    eval_accuracy2(preds,golds)

        
    
    
    
    

def readInputAndOutput(output,input,op,ip):
    
    f1 = open(output + op)
    lines = f1.readlines()
    preds = [ line.split()[0] for line in lines]
    f1.close()
    
    f1 = open(input +ip)
    f1.readline()
    lines = f1.readlines()
    golds = [ line.split()[0] for line in lines]
    f1.close()

    eval_accuracy2(preds,golds)
    
def readOutputTao(output,op,target):
    
    f1 = open(output + op)
    lines = f1.readlines()
    preds = [ line.split()[0] for line in lines]
    golds = [ line.split()[1] for line in lines]
    f1.close()
    
    eval_accuracy2(preds,golds)

def eval_accuracy2(preds,golds):
    
    pos= 1
    pos_total = 0
    pos_correct = 0
    pos_pred_total = 0
    for p,g in zip(preds,golds):
        if int(g) == pos:
            pos_total += 1
        if int(p) == pos:
            pos_pred_total +=1
        if int(g) == pos and int(p) == pos :
                 pos_correct += 1
    
  #  print 'Pos total: ' + str(pos_total), 'Pos correct: ' + str(pos_correct),  'Pos predicted: ' + str(pos_pred_total)
    precision = pos_correct/float(pos_pred_total) if (pos_pred_total > 0) else 0
    recall = pos_correct/float(pos_total)
    f_score = 2 * precision * recall / (precision + recall) if (precision > 0 and recall > 0) else 0
    
    global total_f1
    total_f1 =  total_f1 + f_score
    
    print 'precision:' + '\t' + str(precision*100) + '\t' + 'recall:' + '\t'+ str(recall*100) + '\t' +  'f_score:' + '\t' + str(f_score*100)

def eval_accuracy( preds, golds):
        fine = sum([ sum(int(p) == int(y)) for p,y in zip(preds, golds) ]) + 0.0
        fine_tot = sum( [ len(y) for y in golds ] )
        pos_total = 0
        pos_correct = 0
        pos_pred_total = 0
        pos = '1'
        for ps, ys in zip(preds, golds):
             for p, y in zip(ps, ys):
                if y == self.vocaby[pos]:
                    pos_total += 1
                if p == self.vocaby[pos]:
                    pos_pred_total += 1
                if y == self.vocaby[pos] and p == self.vocaby[pos]:
                    pos_correct += 1
        print 'Pos total: ' + str(pos_total), 'Pos correct: ' + str(pos_correct),  'Pos predicted: ' + str(pos_pred_total)
        precision = pos_correct/float(pos_pred_total) if (pos_pred_total > 0) else 0
        recall = pos_correct/float(pos_total)
        f_score = 2 * precision * recall / (precision + recall) if (precision > 0 and recall > 0) else 0
        return fine/fine_tot, precision, recall, f_score
    

def loadTargets():
   # path = '../../vector/data/config/'
    path = './data/config/'
    file = 'targets.txt'
    f = open(path + file)
    targets = [line.strip() for line in f.readlines() ]
    return targets

if __name__=="__main__":
      
    mainPath = "./auto-grader/ArgumentDetection/"
    pdtbPath = 'data/pdtb/input/'
    technoratiPath = 'data/technorati/input/'

    op = 'comparison_sr.op'
    ip = 'sr_train_all_nowindow_11182014.txt.classification.posn.new.alldata'
    output = mainPath + pdtbPath
    input = mainPath + technoratiPath
    baselineHeuristic(input,ip)
#    readInputAndOutput(output,input,op,ip)
    
   # print 'avg f1 is ' + str(total_f1/len(targets) )
    