# lib of MiMC

import sys 
sys.path.append("..")

from basic.basic import queryFalse, xorOperation, powerOperation,startSATsolver,solveSTP

def gcd(a,b):
    while a != 0:
        a,b = b%a, a
    return b

def findModReverse(a,m):
    if gcd(a,m) != 1:
        print("Invalid block size!")
        return none
    
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    
    while v3 != 0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1), (u2-q*v2), (u3-q*v3), v1,v2,v3
    print(u1%m)
    
    return u1 % m

###################################################################

######################## generate stp file ########################

###################################################################


'''
[genVariable] : generate variables and auxiliary variables

'''

def genVariable(n,r,fw):
    command = ""
    for i in range(r+1):
        command += "x" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    
    for i in range(r+1):
        command += "y" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    
    for i in range(r+1):
        command += "k" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    command += "\n"
    fw.write(command)

'''
[genWeightVariable] : generate weight variables 

'''

def genWeightVariable(n,r,fw):

    addstr = "0bin" + "0".zfill(n-1)
    command = ""
    
    command += "wx : BITVECTOR(" + str(n) + ");\n" 
    command += "ASSERT wx = BVPLUS({}".format(n)
    for b in range(n):
        command += "," + addstr + "@(x0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "\n"
   
    fw.write(command)


'''
[rangeVariable] : set range of variables

'''

def rangeVariable(n,r,fw):
    command = ""

    degree_str = "{:b}".format(pow(2,n)-1)
    degree_str = "0bin" + degree_str.zfill(n)

    for i in range(r+1):
        command += "ASSERT BVLE( x" + str(i) + ", " + degree_str + ");\n"
    command += "\n"
    for i in range(r+1):
        command += "ASSERT BVLE( y" + str(i) + ", " + degree_str + ");\n"
    command += "\n"
    for i in range(r+1):
        command += "ASSERT BVLE( k" + str(i) + ", " + degree_str + ");\n"
    command += "\n"
    for i in range(r+1):
        command += "ASSERT BVGE( x" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"
    for i in range(r+1):
        command += "ASSERT BVGE( y" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"
    for i in range(r+1):
        command += "ASSERT BVGE( k" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"

    fw.write(command)


'''
[finalConstraint] : set yr = 1

'''    

def finalConstraint(n,r,fw):
    command = "" 
    test_degree = "{:b}".format(1)
    command += "ASSERT y" + str(r) + " = 0bin" + test_degree.zfill(n) + ";\n\n"; 

    fw.write(command)

'''
[roundConstraint]:
    - set the round constraint 
    - block size     : n
    - round number   : r
    - round function : (x+k)**d
'''
def roundConstraint(n,r,d,fw):

    command = ""
    upstr   = "{:b}".format(pow(2,n)-1)
    downstr = str(0)
    upstr   = upstr.zfill(n)
    downstr = downstr.zfill(n)

    for i in range(0,r+1):

        strIn = [0,0]
        strIn[0] = "x{}".format(i)
        strIn[1] = "k{}".format(i)
        strOut = "y{}".format(i)
        command = xorOperation(strIn,strOut,n,command)
        command += ""

        if i < r:
            strIn  = "y{}".format(i)
            strOut = "x{}".format(i+1)
            command = powerOperation(strIn,strOut,n,d,command)
    fw.write(command)

def invRoundConstraint(n,r,d,fw):

    command = ""
    upstr   = "{:b}".format(pow(2,n)-1)
    downstr = str(0)
    upstr   = upstr.zfill(n)
    downstr = downstr.zfill(n)

    for i in range(0,r+1):

        strIn = [0,0]
        strIn[0] = "x{}".format(i)
        strIn[1] = "k{}".format(i)
        strOut = "y{}".format(i)
        command = xorOperation(strIn,strOut,n,command)
        command += ""

        if i < r:
            strIn  = "y{}".format(i)
            strOut = "x{}".format(i+1)
            command = powerOperation(strOut,strIn,n,d,command)
    fw.write(command)
