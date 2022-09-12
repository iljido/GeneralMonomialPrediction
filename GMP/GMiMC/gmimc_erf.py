import math
import subprocess
import time
import os
import sys

sys.path.append("..")

from basic.basic import queryFalse, startSATsolver,solveSTP
from GMiMC.gmimc_erf_lib import genVariable, genWeightVariable, rangeVariable,  finalConstraint, roundConstraint


# path of stp and cryptominisat
PATH_CRYPTOMINISAT = "/usr/local/bin/cryptominisat5"
PATH_STP = "/usr/local/bin/stp"


# Search the degree of GMiMC_erf with the set of branches xi
#   - mode = i : the ith branch 
#   - xi       : the set of branches

def searchMonomialxi(n,r,d,testweight,mode,xi):
    #print("Test weight : {}".format(testweight))
    stp_file = "./tmp/gmimc_block_%s"%n + "_r%s"%(r) + "_x%s"%(xi) + ".cvc"
    
    fw = open(stp_file,"w")

    command = "%Block size: " + str(n) + "\n%Round = " + str(r) + "\n%Test weight " + "\n"
    
    # generate stp file
    fw.write(command)
    genVariable(n,r,fw)
    genWeightVariable(n,r,fw)
    rangeVariable(n,r,fw)
    finalConstraint(n,r,fw,mode)
    roundConstraint(n,r,d,fw)
    lenwx = math.ceil(math.log(n)/math.log(2))+3
    lenwk = math.ceil(math.log(n*r)/math.log(2))+1
    testdegree = "{:b}".format(testweight)
    #testdegree = testdegree.zfill(lenwx)
    testdegree = testdegree.zfill(lenwk)


     # initial constraints
    command = "ASSERT wk{} = 0bin".format(xi) + testdegree + ";\n"
    fw.write(command)
    queryFalse(fw)
    fw.close()

    result = solveSTP(stp_file)
    os.remove(stp_file)

    if "Invalid" in result:
        #print("Exist monomial x of weight {}!".format(testweight))
        return 1
    else:
        #print("Non-exsit monomial x of weight {}!".format(testweight))
        return 0


# GMiMC[33,8,56]
d = 3
n = 11
t = 4
mode = 0
#xi = "567"
xi = ""
Round = 56
print("Block size : ", n )
print("Max round number : {}\n".format( Round ))


for testRound in range(1, Round + 1):

    R0 = math.log(pow(2,n-1))/math.log(d) + t-1
    '''
    if testRound < R0:
        if testRound > 5:
            maxdegree50 = min(math.floor(math.log(pow(d,testRound-5)+1)/math.log(2)),n)
        elif testRound == 5:
            maxdegree50 = 1
        else:
            maxdegree50 = 0

        if testRound > 6:
            maxdegree60 = min(math.floor(math.log(pow(d,testRound-6)+1)/math.log(2)),n)
        elif testRound == 6:
            maxdegree60 = 1
        else:
            maxdegree60 = 0

        if testRound > 7:
            maxdegree70 = min(math.floor(math.log(pow(d,testRound-7)+1)/math.log(2)),n)
        elif testRound == 7:
            maxdegree70 = 1
        else:
            maxdegree70 = 0
        maxdegree = maxdegree50 + maxdegree60 + maxdegree70
    else:
        maxdegree = 3*n-1
        maxdegree50 = n
        maxdegree60 = n
        maxdegree70 = n

    print("maxdegree : {}\t maxdegree50 : {}\t maxdegree60 : {}\t maxdegree70 : {}".format(maxdegree,maxdegree50,maxdegree60,maxdegree70))
    '''
    #for testweight in range(maxdegree,0,-1):
    lastflag = 0
    flag = 0
    for testweight in range(1,n*t):  
        lastflag = flag
        flag = searchMonomialxi(n,testRound,d,testweight,mode,xi)
        if (lastflag==1) and (flag == 0) :
            print("Test round : {}\tWeight of x{} = {}".format(testRound,xi, testweight-1))
            #print("==========================")
            break

    '''

    for testweight in range(maxdegree50,0,-1):
       
        flag = searchMonomialxi(n,testRound,d,testweight,mode,"5")
        if (flag == 1) :
            print("Test round : {}\tWeight of x5 = {}".format(testRound,testweight))
            print("==========================")
            break

    for testweight in range(maxdegree60,0,-1):
       
        flag = searchMonomialxi(n,testRound,d,testweight,mode,"6")
        if (flag == 1) :
            print("Test round : {}\tWeight of x6 = {}".format(testRound,testweight))
            print("==========================")
            break

    for testweight in range(maxdegree70,0,-1):
       
        flag = searchMonomialxi(n,testRound,d,testweight,mode,"7")
        if (flag == 1) :
            print("Test round : {}\tWeight of x7 = {}".format(testRound,testweight))
            print("==========================")
            break

    ''' 



    
