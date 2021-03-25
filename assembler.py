def assemble(file_name):
    f = open(file_name + ".asm", "r")
    run1 = open(file_name + ".asm", "r")
    count = 16
    lineCount = 0

    for c in run1:
        c = c.strip()
        if(skipOrStay(c) == False):
            continue

        if(instructionType(c) == "skip"):
            symbolDict["@" + c[1:-1]] = str(lineCount)
            lineCount -= 1
        lineCount += 1

    writer = open(file_name + ".hack", "w")
    for x in f:
        x = x.strip()
        #check if comment or blank line
        if(skipOrStay(x) == False):
            continue
        #A-instruction or C-instruction
        if(instructionType(x) == "aInstruction"):
            x = x.replace("@","")
            x = int(x, base=10)
            x = str(decimalToBinary(x))
            while len(x) < 16:
                x = "0" + x
            writer.write(x + "\n") 
        elif(instructionType(x) == "sInstruction"):
            getNumber = symbolDict.get(x)
            if (getNumber == None):
                symbolDict[x] = str(count)
                getNumber = str(decimalToBinary(count))
                count += 1   
            else:
                getNumber = str(decimalToBinary(int(getNumber)))
            while len(getNumber) < 16:
                getNumber = "0" + getNumber
            writer.write(getNumber +"\n")
        elif(instructionType(x) == "skip"):
            continue
        else:
            strStart = "111"
            if "=" not in x:
                dest = "000"
            else:
                dest = x.split("=")[0]
                x = (x.split("=")[1]).strip()
                #dictionary of dest. equivalent binary
                destBinary = {
                    "M" : "001",
                    "D" : "010",
                    "MD" : "011",
                    "A" : "100",
                    "AM" : "101",
                    "AD" : "110",
                    "AMD" : "111"
                }
                dest = destBinary.get(dest)
            if ";" not in x:
                jump = "000"
            else:
                jump = x.split(";")[1].strip()
                x = (x.split(";")[0]).strip()
                #dictionary of jmp. equivalent binary
                jmpBinary = {
                    "JGT" : "001",
                    "JEQ" : "010",
                    "JGE" : "011",
                    "JLT" : "100",
                    "JNE" : "101",
                    "JLE" : "110",
                    "JMP" : "111"
                }
                jump = jmpBinary.get(jump)
            compBinary = {
                "0" : "0101010",
                "1" : "0111111",
                "-1" : "0111010",
                "D" : "0001100",
                "A" : "0110000",
                "!D" : "0001101",
                "!A" : "0110001",
                "-D" : "0001111",
                "-A" : "0110011",
                "D+1" : "0011111",
                "A+1" : "0110111",
                "D-1" : "0001110",
                "A-1" : "0110010",
                "D+A" : "0000010",
                "D-A" : "0010011",
                "A-D" : "0000111",
                "D&A" : "0000000",
                "D|A" : "0010101",
                "M" : "1110000",
                "!M" : "1110001",
                "-M" : "1110011",
                "M+1" : "1110111",
                "M-1" : "1110010",
                "D+M" : "1000010",
                "D-M" : "1010011",
                "M-D" : "1000111",
                "D&M" : "1000000",
                "D|M" : "1010101"
            }
            comp = compBinary.get(x) 
            
            writer.write(strStart + comp + dest + jump + "\n")


def skipOrStay(line): #checks to see if line is a comment or blank line
    if len(line.strip()) ==0 :
        #return "empty"
        return False
    if "//" in line:
        #return "comment"
        return False
    #return "proceed"
    return True

def instructionType(line): # if symbol @ is in instructions, then its an A type
    if line.find("@") == 0:
        tempLine = line.split("@")[1].strip()
        if tempLine.isdigit():
            return "aInstruction" 
        return "sInstruction"
    if line.find("(") == 0:
        return "skip"
    return "cInstruction" 

def decimalToBinary(n):
    return bin(n).replace("0b","")



symbolDict ={
    "@SP" : 0,
    "@LCL" : 1,
    "@ARG" : 2,
    "@THIS" : 3,
    "@THAT" : 4,
    "@R0" : 0,
    "@R1" : 1,
    "@R2" : 2,
    "@R3" : 3,
    "@R4" : 4,
    "@R5" : 5,
    "@R6" : 6,
    "@R7" : 7,
    "@R8" : 8,
    "@R9" : 9,
    "@R10" : 10,
    "@R11" : 11,
    "@R12" : 12,
    "@R13" : 13,
    "@R14" : 14,
    "@R15" : 15,
    "@SCREEN" : 16384,
    "@KBD" : 24576

}

filetoRead = input("Please enter name of the file(no file extension): \n")
assemble(filetoRead)