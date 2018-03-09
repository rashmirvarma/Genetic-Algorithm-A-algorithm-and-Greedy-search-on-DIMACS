try:
    from pyevolve import G1DList, GAllele
except:
    ImportError
try:
    from pyevolve import GSimpleGA
except:
    ImportError
try:   
    from pyevolve import Mutators
except:
    ImportError
try:
    from pyevolve import Crossovers
except:
    ImportError
try:
    from pyevolve import Consts
except:
    ImportError
try:
    from pyevolve import Initializators
except:
    ImportError
try:
    import sys, random
except:
    ImportError
try:
    from math import sqrt
except:
    ImportError


LAST_SCORE = -1

##Function to compute x1,x2,x3 and x4 for decision tree
def computeX (arr, x0):
    if arr[x0][1] == 0 and arr[x0][2] == 0:
        x = "x1"
    if arr[x0][1] == 0 and arr[x0][2] == 1:
        x = "x2"
    if arr[x0][1] == 1 and arr[x0][2] == 0:
        x = "x3"
    if arr[x0][1] == 1 and arr[x0][2] == 1:
        x = "x4"
    return x

##Function to calculate the value based on the last three digits of string
def computeVal(arr,x):
    val = x
    if arr[x][3] == 0 and arr[x][4] == 0 and arr[x][5] == 0:
        val = 0
    if arr[x][3] == 0 and arr[x][4] == 0 and arr[x][5] == 1:
        val = 1
    if arr[x][3] == 0 and arr[x][4] == 1 and arr[x][5] == 0:
        val = 2
    if arr[x][3] == 0 and arr[x][4] == 1 and arr[x][5] == 1:
        val = 3
    if arr[x][3] == 1 and arr[x][4] == 0 and arr[x][5] == 0:
        val = 4
    if arr[x][3] == 1 and arr[x][4] == 0 and arr[x][5] == 1:
        val = 5
    return val

##Function to compute sign based on first element
def computeSign(arr,x):
    sign = 0
    if arr[x][0]:
        sign = -1
    else:
        sign = 1
    return sign

##Function to predict class
def predict(y,num):
    if y<num:
        return "w1"
    else:
        return "w2"

##Function to calculate right subtree of decision tree
def findRightSubTree(y,p,val,sign,num):
    x = "null"
    if y<num:        
        x  = computeX(p,5)
        val = computeVal(p,5)
        sign = computeSign(p,5)
        num = val*sign
        if x=="x1":
            return predict(y,num)
        elif x=="x2":
            return predict(y,num)
        elif x=="x3":
            return predict(y,num)
        else:
            return predict(y,num)
    else:
        x  = computeX(p,6)
        val = computeVal(p,6)
        sign = computeSign(p,6)
        num = val*sign
        if x=="x1":
            return predict(y,num)
        elif x=="x2":
            return predict(y,num)
        elif x=="x3":
            return predict(y,num)
        else:
            return predict(y,num)

##Function to calculate left sub tree of the decision tree
def findLeftSubTree(y,p,val,sign,num):
    x = "null"

    if y<num:
        
        x  = computeX(p,0)
        val = computeVal(p,0)
        sign = computeSign(p,0)
        num = val*sign
        if x=="x1":
            return predict(y,num)
        elif x=="x2":
            return predict(y,num)
        elif x=="x3":
            return predict(y,num)
        else:
            return predict(y,num)
    else:
        x  = computeX(p,1)
        val = computeVal(p,1)
        sign = computeSign(p,1)
        num = val*sign
        if x=="x1":
            return predict(y,num)
        elif x=="x2":
            return predict(y,num)
        elif x=="x3":
            return predict(y,num)
        else:
            return predict(y,num)

##Function to calculate tree
def findTree(y,p,val,sign,num):
    x = "null"

    
    if y<num:
        x  = computeX(p,2)
        val = computeVal(p,2)
        sign = computeSign(p,2)
        num = val*sign
        if x=="x1":
            return findLeftSubTree(y,p,val,sign,num)
        if x=="x2":
            return findLeftSubTree(y,p,val,sign,num)

        if x=="x3":
            return findLeftSubTree(y,p,val,sign,num)

        else:
            return findLeftSubTree(y,p,val,sign,num)
    else:
        x  = computeX(p,4)
        val = computeVal(p,4)
        sign = computeSign(p,4)
        num = val*sign
        if x=="x1":
            return findRightSubTree(y,p,val,sign,num)
        if x=="x2":
            return findRightSubTree(y,p,val,sign,num)

        if x=="x3":
            return findRightSubTree(y,p,val,sign,num)

        else:
            return findRightSubTree(y,p,val,sign,num)       

##Function to create tree            
def decTree(chromString,y1,y2,y3,y4):

    p = []
    val = 0
    n = 6
    x = "null"
    actual = "null"
    line = chromString
    p = [line[i:i+n] for i in range(0, len(line), n)]
    
    val = computeVal(p,3)
    sign = computeSign(p,3)
    num = val*sign

    x  = computeX(p,3)

    if x=="x1":
        actual = findTree(y1,p,val,sign,num)
    if x=="x2":
        actual = findTree(y2,p,val,sign,num)

    if x=="x3":
        actual = findTree(y3,p,val,sign,num)

    if x=="x4":
        actual = findTree(y4,p,val,sign,num)

    print ("The predicted class is: {}".format(actual))
    return

##Input function
def findCoords():
    y1= 0
    y2=0
    y3=0
    y4=0
    y1 = int(raw_input("Please enter x1:"))
    y2 = int(raw_input("Please enter x2:"))
    y3 = int(raw_input("Please enter x3:"))
    y4 = int(raw_input("Please enter x4:"))

    return y1,y2,y3,y4

##Function to create CLI   
def evaluate(chromosome):
    flag = 0
    choice = 0
    while(flag == 0):
        try:
            choice = int(raw_input("\n0. Quit \n1.Enter string to classify \n2. View results of the three strings mentioned in the Excellent section \nYour choice:"))
            if choice == 0:
                break
            if choice == 1:
                y1,y2,y3,y4 = findCoords()
                decTree(chromosome,y1,y2,y3,y4)
            if choice == 2:
                print "For -1,4,1,1 the classification is as follows:"
                decTree(chromosome,-1,4,1,1)
                print "For -2,4,-1,1 the classification is as follows:"
                decTree(chromosome,-2,4,-1,1)
                print "For 3,3,0,1 the classification is as follows:"
                decTree(chromosome,3,3,0,1)
            else:
                print("Please choose from the list")
        except:
            print("A problem occurred. Please run the code again")
     

def main_run():
   genome = G1DList.G1DList(42)

   genome.evaluator.set(lambda chromosome: evaluate(chromosome.getInternalList()))
   genome.crossover.set(Crossovers.G1DListCrossoverEdge)
   genome.initializator.set(Initializators.G1DBinaryStringInitializator)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(500)
   ga.setMinimax(Consts.minimaxType["maximize"])
   ga.setCrossoverRate(0.6)
   ga.setMutationRate(0.01)
   ga.setPopulationSize(15)

   try:
       ga.evolve(freq_stats=1000)
   except:
       print("\n")
   best = ga.bestIndividual()
   
   ch = best.genomeList
   evaluate(ch)


if __name__ == "__main__":
   main_run()
