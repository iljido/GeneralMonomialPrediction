import subprocess
import math

'''

Basic Operation:
    - xorOperation(strIn,strOut,n,command)
    - addOperation(strIn,strOut,n,command)
    - copyOperation(strIn,strOut,n,command)
    - generalCopyOperation(strIn,strOut,n,command)
    - powerOperation(strIn,strOut,n,d,command)
    - queryFalse

'''

'''

STP:
    startSATsolver(stp_file)
    solveSTP(stp_file)

'''

PATH_CRYPTOMINISAT = "/usr/local/bin/cryptominisat5"
PATH_STP = "/usr/local/bin/stp"



#============= XOR ==============
def xorOperation(strIn,strOut,n,command):

    command += "ASSERT " + strOut + " = BVPLUS(" + str(n) + "," + strIn[0] + "," + strIn[1] + ");\n"
    command += "ASSERT " + strOut + " & " + strIn[0] + " = " + strIn[0] + ";\n\n"
    
    return command


#============= ADD ==============
def addOperation(strIn,strOut,n,command):

    command += "ASSERT " + strIn[0] + " = " + strOut + ";\n"
    command += "ASSERT " + strIn[1] + " = " + strOut + ";\n"
    command += "\n"

    return command


#============= COPY ==============
def copyOperation(strIn,strOut,n,command):

    downstr = "0".zfill(n)
    strMod = "t_"+ strIn
    command += "{} : BITVECTOR(1);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin0@{}, 0bin0@{}, 0bin{}@{});\n".format(strMod,strIn,n+1,strOut[0],strOut[1],downstr,strMod) 
    command += "ASSERT {}@{} /= 0bin1{};\n".format(strMod,strIn,downstr)

    return command

#============= 7-COPY ==============
def generalCopyOperation(strIn,strOut,n,command):
    
    downstr = "0".zfill(n)
    strMod = "t_"+ strIn
    command += "{} : BITVECTOR(3);\n".format(strMod)
    command += "ASSERT BVLE( {}, 0bin111);\n".format(strMod)
    command += "ASSERT BVGE( {}, 0bin000);\n".format(strMod)

    command += "ASSERT {}@{} = BVPLUS( {} , 0bin000@{}, 0bin000@{}, 0bin000@{}, 0bin000@{},0bin000@{},0bin000@{},0bin000@{},0bin{}@{});\n".format(strMod,strIn,n+3,strOut[0],strOut[1],strOut[2], strOut[3],strOut[4],strOut[5],strOut[6],downstr,strMod) 
    command += "ASSERT (IF {} = 0bin{} THEN {} = 0bin000 ELSE BVGE( {} , 0bin000) ENDIF);\n".format(strIn,downstr,strMod,strMod)
   

    return command


#============= POWER ==============
def powerOperation(strIn,strOut,n,d,command):
    
    lenp = math.floor(math.log(d-1)/math.log(2))+1
    rangep = "{:b}".format(d-1).zfill(lenp)

    strMod = "p_" + strIn
    command += "{} : BITVECTOR({});\n".format(strMod,lenp)

    command += "ASSERT BVLE( {} , 0bin{});\n".format(strMod,rangep)
    command += "ASSERT BVGE( {} , 0bin{});\n".format(strMod,"0".zfill(lenp))

    newlen = n + lenp
    strMul0 = "{:b}".format(d).zfill(newlen)
    strMul1 = "0".zfill(lenp) + "@" + strOut
    strAdd = "0".zfill(n) + "@" + strMod

    command += "ASSERT {}@{} = BVPLUS( {}, BVMULT( {}, 0bin{}, 0bin{} ),0bin{});\n".format(strMod,strIn,newlen,newlen,strMul0,strMul1,strAdd)

    return command

def queryFalse(fw):
    command = "QUERY FALSE;\nCOUNTEREXAMPLE;\n"
    fw.write(command)


###################################################################################


"""
Return CryptoMiniSat process started with the given stp_file.
"""
def startSATsolver(stp_file):

    # Start STP to construct CNF
    subprocess.check_output([PATH_STP, "--exit-after-CNF", "--output-CNF", stp_file, "--CVC", "--disable-simplifications"])
 
    #if test
    # Find the number of solutions with the SAT solver
    sat_params = [ PATH_CRYPTOMINISAT, "--maxsol", str(1000000000 ),
                "--verb", "0", "--printsol", "0", "output_0.cnf"]

    sat_process = subprocess.Popen(sat_params, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return sat_process

'''
Returns the solution for the given SMT problem using STP.
'''
def solveSTP(stp_file):

    stp_parameters = [PATH_STP, stp_file, "--CVC"]
    result = subprocess.check_output(stp_parameters)

    return result.decode("utf-8")