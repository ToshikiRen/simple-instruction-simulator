# Functions module
from constants import *

# Set labels


def setLabel(root, stringVar, font=courier24, anchor="e", justify=LEFT, padx=0,
             width=16):
    return Label(root, textvariable=stringVar, font=font, anchor=anchor,
                 justify=justify, padx=padx)

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
        returnString += regString[2*i: 2*i + 2]
        if i < 3:
            returnString += ' '

    return returnString


def printRegString():

    for reg in list_regs:
        print(regs_dict[reg][0])


def readRegisters(mu):

    for i in range(0, number_of_regs):
        regs_dict[list_regs[i]][0] = formatRegisterString(
            hex(mu.reg_read(list_regs_x86[i])), list_regs[i])
        regs_dict[list_regs[i]][0] = regs_dict[list_regs[i]][0].upper()


def initializeRegisters(mu, listOfValues):

    for i in range(number_of_regs):
        mu.reg_write(list_regs_x86[i], listOfValues[i])


def setRegsName():

    for i in range(number_of_regs):
        list_regs_string[i].set(list_regs[i] + ': ')


def runInstruction_old(instr, mu, ADDRESS):

    global instr_code
    instr = instr.replace(" ", "")
    instr = instr.replace("\n", '')
    instr = instr.lower()
    try:
        print(instr, end='\n')
        instr_code = instruction_set_arch[instr]
        print(instr_code, end='\n')
    except:
        instr_code = -1

    if instr_code != -1:
        instr = bytes(instr_code, 'UTF-8')
        mu.mem_write(ADDRESS, instr)
        runInstructionOn(mu, ADDRESS, instr)
        instr_code = -1
        readRegisters(mu)
        updateStrVar()
        # printRegString()


def runInstruction(instr, mu, ADDRESS):

    instr = instr.replace("\n", '')
    print(instr)
    # instance of Keystone
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        instr_code, count = ks.asm(instr)
        instr = bytes()

        for x in instr_code:
            instr = instr + bytes([x])
        instr_code = instr

    except KsError as e:
        print("Error: %s", e)
        instr_code = -1

    if instr_code != -1:
        try:
            print(ADDRESS)
            mu.mem_write(ADDRESS, instr)

        except:
            print("Memory write FAILED!!")
        runInstructionOn(mu, ADDRESS, instr)

        read_mem_format(mu, ADDRESS, MEM_SIZE)
        instr_code = -1
        readRegisters(mu)
        updateStrVar()
        # printRegString()


def hook_mem(uc, access, address, size, value, user_data):

    pass


def my_hex(to_hex):

    if to_hex == 0:
        return "00"
    else:
        return hex(to_hex)[2:]


# Formats the adress range for display purposes
def add_address_range(start_address, per_row, max_len):

    end_addr = start_address
    end_addr += per_row
    start = str(start_address)
    end = str(end_addr)

    start = (max_len - len(start)) * '0' + start
    end   = (max_len - len(end)) * '0' + end

    return start + '->' + end + ': '


def read_mem_format(mu, start_address, quantity, per_row = 24):

    mem = mu.mem_read(start_address, quantity)
    mem_data = ''
    max_len = len(str(start_address + quantity))
    for i in range(0, quantity//per_row):
        mem_data += add_address_range(start_address, per_row, max_len)
        start_address += per_row
        mem_data += " ".join([my_hex(x)
                              for x in (mem[i * per_row: per_row * (i + 1)])])
        mem_data += '\n'

    return mem_data
    # for byte in reversed(mem):
    #    print(hex(byte), end = "")
    # print("")
    # print(mu.reg_read(UC_X86_REG_DS))


def setupUI():

    pass


def runInstructionOn(mu, address, instr_code):

    mu.emu_start(address, address + len(instr_code))


# Tkinter

# Scrollable window
def openWindow(title, size):

    newWindow = Toplevel(root)
    newWindow.geometry(size)
    newWindow.title(title)
    # newWindow.resizable(0, 0)
    # Create a frame for the canvas
    main_frame = Frame(newWindow)
    main_frame.pack(fill = BOTH, expand = 1)

    # Adding the canvas
    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill = BOTH, expand = 1)

    # Adding the scrollbar
    scroll = ttk.Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
    scroll.pack(side = RIGHT, fill = Y)

    scrollX = ttk.Scrollbar(newWindow, orient = HORIZONTAL, command = canvas.xview)
    scrollX.pack(side = BOTTOM, fill = X)
    # Canvas configuration
    canvas.configure(yscrollcommand = scroll.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    canvas.configure(xscrollcommand = scrollX.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

    # Secondary frame
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window = second_frame, anchor = "nw")

    return second_frame

def openMemory(mu, start_address=ADDRESS, quantity=MEM_SIZE, title="Memory", size="400x400"):

    global mem
    window = openWindow(title, "800x400")
    mem = read_mem_format(mu, start_address, quantity)
    memStringVar.set(mem)

    updateMeme = Button(window, text = 'Update', command = lambda: updateMemory(mu, ADDRESS, MEM_SIZE))
    updateMeme.grid(row = 0, column = 0, sticky = "nw")
    label = setLabel(window, memStringVar, courier10, anchor="center", justify=LEFT, padx=0,
                     width=16)
    label.grid(row = 1, column = 0)

def updateMemory(mu, address, mem_size):

    mem = read_mem_format(mu, address, mem_size)
    memStringVar.set(mem)