import sys 
sys.path.append("..")

from basic.basic import queryFalse, copyOperation, xorOperation,powerOperation, startSATsolver,solveSTP

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
        command += "x0_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r+1):
        command += "x1_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r):
        command += "k" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

   
    for i in range(r):
        command += "y" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r):
        command += "z" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r):
        command += "l" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    command += "\n"
    fw.write(command)

'''
[genWeightVariable] : generate variables and auxiliary variables
'''

def genWeightVariable(n,r,fw):

    addstr = "0bin" + "0".zfill(n-1)

    command = ""

    command += "wx : BITVECTOR(" + str(n) + ");\n" 
    command += "ASSERT wx = BVPLUS({}".format(n)
    for b in range(n):
        command += "," + addstr + "@(x0_0[{}:{}])".format(b,b)
    for b in range(n):
        command += "," + addstr + "@(x1_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx0 : BITVECTOR(" + str(n) + ");\n" 
    command += "ASSERT wx0 = BVPLUS({}".format(n)
    for b in range(n):
        command += "," + addstr + "@(x0_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx1: BITVECTOR(" + str(n) + ");\n" 
    command += "ASSERT wx1 = BVPLUS({}".format(n)
    for b in range(n):
        command += "," + addstr + "@(x1_0[{}:{}])".format(b,b)
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
        command += "ASSERT BVLE( x0_" + str(i) + ", " + degree_str + ");\n"
    for i in range(r+1):
        command += "ASSERT BVLE( x1_" + str(i) + ", " + degree_str + ");\n"
    for i in range(r):
        command += "ASSERT BVLE( k" + str(i) + ", " + degree_str + ");\n"
    for i in range(r):
        command += "ASSERT BVLE( y" + str(i) + ", " + degree_str + ");\n"
    for i in range(r):
        command += "ASSERT BVLE( z" + str(i) + ", " + degree_str + ");\n"
    for i in range(r):
        command += "ASSERT BVLE( l" + str(i) + ", " + degree_str + ");\n"
    command += "\n"
    
    for i in range(r+1):
        command += "ASSERT BVGE( x0_" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    for i in range(r+1):
        command += "ASSERT BVGE( x1_" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    for i in range(r):
        command += "ASSERT BVGE( k" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    for i in range(r):
        command += "ASSERT BVGE( y" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    for i in range(r):
        command += "ASSERT BVGE( z" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    for i in range(r):
        command += "ASSERT BVGE( l" + str(i) + ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"

    fw.write(command)


'''
[finalConstraint] : set the last variable = 1
'''    

def finalConstraint(n,r,fw,mode):
    command = "" 
    test_degree0 = "{:b}".format(0)
    test_degree1 = "{:b}".format(1)
    
    if mode == 1:
        command += "ASSERT x0_" + str(r) + " = 0bin" + test_degree0.zfill(n) + ";\n\n"; 
        command += "ASSERT x1_" + str(r) + " = 0bin" + test_degree1.zfill(n) + ";\n\n";
    if mode == 0:
        command += "ASSERT x0_" + str(r) + " = 0bin" + test_degree1.zfill(n) + ";\n\n"; 
        command += "ASSERT x1_" + str(r) + " = 0bin" + test_degree0.zfill(n) + ";\n\n";

    fw.write(command)


'''
[roundConstraint]:
    - set the round constraint 
    - round number : r
    - round : (x+k)**d
'''

def roundConstraint(n,r,d,fw):

    command = ""
    invstr = "{:b}".format(d)
    invstr = invstr.zfill(n)
    upstr   = "{:b}".format(pow(2,n)-1)
    downstr = str(0)
    upstr   = upstr.zfill(n)
    downstr = downstr.zfill(n)

    for i in range(0,r):

        # copy
        strIn   = "x0_{}".format(i)
        strOut = [0 for _ in range(2)]
        strOut[0] = "x1_{}".format(i+1)
        strOut[1] = "y{}".format(i)
        command = copyOperation(strIn,strOut,n,command)
        command += "\n"

        # xor key
        strIn = [0,0]
        strIn[0] = "y{}".format(i)
        strIn[1] = "k{}".format(i)
        strOut = "z{}".format(i)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        # x^3
        strIn = "z{}".format(i)
        strOut = "l{}".format(i)
        command = powerOperation(strIn,strOut,n,d,command)
        command += "\n"

        # xor 
        strIn = [0,0]
        strIn[0] = "l{}".format(i)
        strIn[1] = "x1_{}".format(i)
        strOut = "x0_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"
    fw.write(command)


