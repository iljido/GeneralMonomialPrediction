import math
import subprocess
import time
import os
import sys

sys.path.append("..")

from basic.basic import queryFalse, startSATsolver,solveSTP
from Feistel_MiMC.feistel_mimc_lib import genVariable, genWeightVariable, rangeVariable,  finalConstraint, roundConstraint

# path of stp and cryptominisat
PATH_CRYPTOMINISAT = "/usr/local/bin/cryptominisat5"
PATH_STP = "/usr/local/bin/stp"


# Search the algebraic degree of Feistel MiMC
#   - mode = 0 : the left branch 
#   - mode = 1 : the right branch

def searchMonomialx(n,r,d,testweight,mode):
    stp_file = "./tmp/feistel_mimc_block_%s"%n + "_r%s"%(r) + "_x.cvc"
    
    fw = open(stp_file,"w")

    command = "%Block size: " + str(n) + "\n%Round = " + str(r) + "\n%Test weight " + "\n"
    
    # generate stp file
    fw.write(command)
    genVariable(n,r,fw)
    genWeightVariable(n,r,fw)
    rangeVariable(n,r,fw)

    finalConstraint(n,r,fw,mode)
    roundConstraint(n,r,d,fw)

    testdegree = "{:b}".format(testweight)
    testdegree = testdegree.zfill(n)

     # initial constraints
    command = "ASSERT wx = 0bin" + testdegree + ";\n"
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


# Search the univariate degree of Feistel MiMC
#   - mode = 0 : the left branch 
#   - mode = 1 : the right branch
#   - xi   = 0 : search univariate degree if x0
#   - xi   = 1 : search univariate degree if x1

def searchMonomialxi(n,r,d,testweight,mode,xi):
    
    stp_file = "./tmp/feistel_mimc_block_%s"%n + "_r%s"%(r) + "x%s"%(xi) + ".cvc"
    
    fw = open(stp_file,"w")

    command = "%Block size: " + str(n) + "\n%Round = " + str(r) + "\n%Test weight " + "\n"
    
    # generate stp file
    fw.write(command)
    genVariable(n,r,fw)
    genWeightVariable(n,r,fw)
    rangeVariable(n,r,fw)
    finalConstraint(n,r,fw,mode)
    roundConstraint(n,r,d,fw)

    testdegree = "{:b}".format(testweight)
    testdegree = testdegree.zfill(n)

    # initial constraints
    command = "ASSERT wx{} = 0bin".format(xi) + testdegree + ";\n"
    fw.write(command)
    queryFalse(fw)
    fw.close()

    result = solveSTP(stp_file)
    os.remove(stp_file)


    if "Invalid" in result:
        #print("Exist monomial x{} of weight {}!".format(xi,testweight))
        return 1
    else:
        #print("Non-exsit monomial x{} of weight {}!".format(xi,testweight))
        return 0


d = 3
n = 129
mode = 0
Round = math.ceil(2 * n * math.log(2)/math.log(d))+3
print("Block size : ", n )
print("Max round number : {}\n".format( Round ))

for testRound in range(1, Round + 1):

    R0 = math.log(pow(2,n-1))/math.log(d) + 1
    if testRound < R0:
        maxdegree00 = min(math.floor(math.log(pow(d,testRound)+1)/math.log(2)),n)
        maxdegree10 = min(math.floor(math.log(pow(d,testRound-1)+1)/math.log(2)),n)
        maxdegree = maxdegree00 + maxdegree10
    else:
        maxdegree = 2*n-1
        maxdegree00 = n
        maxdegree10 = n

    print("maxdegree : {}\t maxdegree00 : {}".format(maxdegree,maxdegree00))
    for testweight in range(maxdegree,0,-1):
       
        flag = searchMonomialx(n,testRound,d,testweight,mode)
        if (flag == 1) :
            print("Test round : {}\tWeight of x = {}".format(testRound,testweight))
            #print("==========================")
            break


    for testweight in range(maxdegree00,0,-1):
       
        flag = searchMonomialxi(n,testRound,d,testweight,mode,0)
        if (flag == 1) :
            print("Test round : {}\tWeight of x0 = {}".format(testRound,testweight))
            print("==========================")
            break







