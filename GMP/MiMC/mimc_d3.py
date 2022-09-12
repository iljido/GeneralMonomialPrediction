import math
import subprocess
import time
import os
import sys 
sys.path.append("..")

from basic.basic import queryFalse, startSATsolver,solveSTP
from MiMC.mimc_lib import genVariable, genWeightVariable, rangeVariable, finalConstraint, roundConstraint,gcd

# path of stp and cryptominisat
PATH_CRYPTOMINISAT = "/usr/local/bin/cryptominisat5"
PATH_STP = "/usr/local/bin/stp"

 
# search the algebraic degree of MiMC

def searchMonomial(n,r,d,testweight):
    stp_file = "./tmp/mimc_block_%s"%n + "_d%s"%(d) + "_r%s"%(r)+".cvc"
    
    fw = open(stp_file,"w")

    command = "%Block size: " + str(n) + "\n%Round = " + str(r) + "\n%Test weight " + "\n"
    
    # generate stp file
    fw.write(command)
    genVariable(n,r,fw)
    genWeightVariable(n,r,fw)
    rangeVariable(n,r,fw)
    finalConstraint(n,r,fw)
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
        print("Exsit x^({})".format(testweight))
        return 1
    else:
        #print("Non-exsit x^({})".format(testweight))
        return 0


        

d = 3
n = 129
Round = math.ceil(n * math.log(2)/math.log(d))
print("Block size : ", n )
print("Max round number : {}\n".format( Round ))

if (gcd(pow(2,n)-1,d)) == 1:

    for testRound in range(80, Round + 1):
        
        print("Test round number : ", testRound )
        
        if testRound <= 81:
            maxdegree = math.floor (math.log(pow(d,testRound)+1)/math.log(2))
        else:
            maxdegree = n-1
        for testweight in range(maxdegree,0,-1):
            #print("Test weight : ",testweight)
            flag = searchMonomial(n,testRound,d,testweight)
            if (flag == 1) :
                print("Test round : {}\tWeight = {}\n".format(testRound,testweight))
                print("==========================")
                break



