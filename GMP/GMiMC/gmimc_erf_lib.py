import sys 
import math
sys.path.append("..")

from basic.basic import queryFalse, copyOperation, xorOperation, powerOperation, generalCopyOperation, startSATsolver,solveSTP

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
    
    # variables
    for i in range(r+1):
        command += "x0_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x1_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x2_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x3_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x4_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x5_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x6_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r+1):
        command += "x7_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r):
        command += "k" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    # auxiliary variables
    for i in range(r):
        command += "y" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "z" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    for i in range(r):
        command += "t0_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t1_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t2_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t3_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t4_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t5_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t6_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"
    for i in range(r):
        command += "t7_" + str(i) + ": BITVECTOR(" + str(n) + ");\n" 
    command += "\n"

    
    command += "\n"
    fw.write(command)


'''
[genWeightVariable]
    + generate variables and auxiliary variables
'''

def genWeightVariable(n,r,fw):

    command = ""

    # wx
    lenwx = math.ceil(math.log(n)/math.log(2))+3
    addstr = "0bin" + "0".zfill(lenwx-1)

    # wk
    lenwk = math.ceil(math.log(n*r)/math.log(2))+1
    newaddstr = "0bin" + "0".zfill(lenwk-1)

    for i in range(r):
        command += "wk{} : BITVECTOR(".format(i) + str(lenwk) + ");\n"
        command += "ASSERT wk{} = BVPLUS({}".format(i,lenwk)
        for b in range(n):
            command += "," + newaddstr + "@(k{}[{}:{}])".format(i,b,b)
        command += ");\n\n"
        command += "\n"

    command += "wk : BITVECTOR(" + str(lenwk) + ");\n"
    if r > 1:
        command += "ASSERT wk = BVPLUS({}".format(lenwk)
        for b in range(r):
            command += ", wk{}".format(b)
        command += ");\n\n"
        command += "\n"
    else:
        command += "ASSERT wk = wk0;\n"
    
    command += "wx0 : BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx0 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x0_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"
    
    command += "wx1: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx1 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x1_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx2: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx2 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x2_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx3: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx3 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x3_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"
    
    command += "wx4 : BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx4 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x4_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx5: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx5 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x5_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx6: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx6 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x6_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"

    command += "wx7: BITVECTOR(" + str(lenwx) + ");\n" 
    command += "ASSERT wx7 = BVPLUS({}".format(lenwx)
    for b in range(n):
        command += "," + addstr + "@(x7_0[{}:{}])".format(b,b)
    command += ");\n\n"
    command += "\n"
   
    command += "wx : BITVECTOR(" + str(lenwx) + ");\n"
    command += "ASSERT wx = BVPLUS({}".format(lenwx)
    for b in range(8):
        command += ", wx{}".format(b)
    command += ");\n\n"
    command += "\n"

    command += "wx567 : BITVECTOR(" + str(lenwx) + ");\n"
    command += "ASSERT wx567 = BVPLUS({}".format(lenwx)
    for b in range(5,8):
        command += ", wx{} ".format(b)
    command += ");\n\n"
    
    command += "\n"


    fw.write(command)


'''
[rangeVariable]
    + set range of variables
'''

def rangeVariable(n,r,fw):
    command = ""
    downstr = "0".zfill(n)
    degree_str = "{:b}".format(pow(2,n)-1)
    degree_str = "0bin" + degree_str.zfill(n)

    for i in range(r+1):
        command += "ASSERT BVLE( x0_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x1_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x2_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x3_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x4_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x5_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x6_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( x7_" + str(i) + ", " + degree_str + ");\n"

    for i in range(r):
        command += "ASSERT BVLE( k" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( y" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( z" + str(i) + ", " + degree_str + ");\n"

    for i in range(r):
        command += "ASSERT BVLE( t0_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t1_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t2_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t3_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t4_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t5_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t6_" + str(i) + ", " + degree_str + ");\n"
        command += "ASSERT BVLE( t7_" + str(i) + ", " + degree_str + ");\n"
   
    command += "\n"
    
    for i in range(r+1):
        command += "ASSERT BVGE( x0_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x1_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x2_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x3_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x4_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x5_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x6_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( x7_" + str(i) + ", 0bin" + downstr + ");\n"

    for i in range(r):
        command += "ASSERT BVGE( k" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( y" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( z" + str(i) + ", 0bin" + downstr + ");\n"

    for i in range(r):
        command += "ASSERT BVGE( t0_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t1_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t2_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t3_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t4_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t5_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t6_" + str(i) + ", 0bin" + downstr + ");\n"
        command += "ASSERT BVGE( t7_" + str(i) + ", 0bin" + downstr + ");\n"
    
    command += "\n"

    fw.write(command)


'''
[finalConstraint]: set the last variable = 1
'''    

def finalConstraint(n,r,fw,mode):
    command = "" 
    test_degree0 = "{:b}".format(0).zfill(n)
    test_degree1 = "{:b}".format(1).zfill(n)
    if mode == 0:
        command += "ASSERT x0_" + str(r) + " = 0bin" + test_degree1 + ";\n\n"; 
        command += "ASSERT x1_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x2_" + str(r) + " = 0bin" + test_degree0 + ";\n\n"; 
        command += "ASSERT x3_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x4_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x5_" + str(r) + " = 0bin" + test_degree0 + ";\n\n"; 
        command += "ASSERT x6_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x7_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";

    if mode == 7:
        command += "ASSERT x0_" + str(r) + " = 0bin" + test_degree0 + ";\n\n"; 
        command += "ASSERT x1_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x2_" + str(r) + " = 0bin" + test_degree0 + ";\n\n"; 
        command += "ASSERT x3_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x4_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x5_" + str(r) + " = 0bin" + test_degree0 + ";\n\n"; 
        command += "ASSERT x6_" + str(r) + " = 0bin" + test_degree0 + ";\n\n";
        command += "ASSERT x7_" + str(r) + " = 0bin" + test_degree1 + ";\n\n";
    fw.write(command)

'''
[roundConstraint]:
    - set the round constraint 
    - round number : r
    - round : (x+k)**d
'''
def roundConstraint(n,r,d,fw):

    command = ""

    for i in range(0,r):

        # copy
        strIn   = "x0_{}".format(i)
        strOut = [0,0]
        strOut[0] = "x7_{}".format(i+1)
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
        strOut = "t0_{}".format(i)
        command = powerOperation(strIn,strOut,n,d,command)

        # general copy
        strIn   = "t0_{}".format(i)
        strOut = [0,0,0,0,0,0,0]
        strOut[0] = "t1_{}".format(i)
        strOut[1] = "t2_{}".format(i)
        strOut[2] = "t3_{}".format(i)
        strOut[3] = "t4_{}".format(i)
        strOut[4] = "t5_{}".format(i)
        strOut[5] = "t6_{}".format(i)
        strOut[6] = "t7_{}".format(i)
        command = generalCopyOperation(strIn,strOut,n,command)

        # xor 
        strIn = [0,0]
        strIn[0] = "t1_{}".format(i)
        strIn[1] = "x1_{}".format(i)
        strOut = "x0_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn[0] = "t2_{}".format(i)
        strIn[1] = "x2_{}".format(i)
        strOut = "x1_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn[0] = "t3_{}".format(i)
        strIn[1] = "x3_{}".format(i)
        strOut = "x2_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn = [0,0]
        strIn[0] = "t4_{}".format(i)
        strIn[1] = "x4_{}".format(i)
        strOut = "x3_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn[0] = "t5_{}".format(i)
        strIn[1] = "x5_{}".format(i)
        strOut = "x4_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn[0] = "t6_{}".format(i)
        strIn[1] = "x6_{}".format(i)
        strOut = "x5_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"

        strIn[0] = "t7_{}".format(i)
        strIn[1] = "x7_{}".format(i)
        strOut = "x6_{}".format(i+1)
        command = xorOperation(strIn,strOut,n,command)
        command += "\n"
    fw.write(command)

