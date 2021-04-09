# Functions module
from constants import *


# Set labels 
def setLabel(root, stringVar, font = courier24, anchor="e", justify=LEFT, padx = 0,
            width = 16):
    return Label(root, textvariable = stringVar, font = font, anchor = anchor, 
        justify = justify, padx = padx)

# Updates the values of the registers from the interface
def updateStrVar():

    for i in range(number_of_regs):
        regs_dict[list_regs[i]][1].set(regs_dict[list_regs[i]][0])

# Formats the register
def formatRegisterString(regString, regName):

    regString = regString.replace('0x', '')
    # returnString = regName + ': '
    returnString = ''
    reg_bytes = len(regString)
    nedded_header = '0' * (8 - reg_bytes)
    regString = nedded_header + regString

    for i in range(0, 4):
        returnString += regString[2*i : 2*i + 2]
        if i < 3:
            returnString += ' '


    return returnString


def printRegString():

    for reg in list_regs:
        print(regs_dict[reg][0])

def readRegisters(mu):
    
    for i in range(0, number_of_regs):
        regs_dict[list_regs[i]][0] = formatRegisterString(hex(mu.reg_read(list_regs_x86[i])), list_regs[i])
        regs_dict[list_regs[i]][0] = regs_dict[list_regs[i]][0].upper()

def initializeRegisters(mu, listOfValues):

    for i in range(number_of_regs):
        mu.reg_write(list_regs_x86[i], listOfValues[i])


def setRegsName():
    
    for i in range(number_of_regs):
        list_regs_string[i].set(list_regs[i] + ': ')

def runInstruction(instr):

    global instr_code
    instr = instr.replace(" ", "")
    instr = instr.replace("\n", '')
    instr = instr.lower()
    try:
        instr_code = instruction_set_arch[instr]
    except:
        instr_code = -1
    
def setupUI():
    
    pass