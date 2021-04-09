# Main program
from utils import *


if "__main__" == __name__:
    
    size = '680x500'

    root.title('x86 Registers')
    root.geometry(size)
    root.resizable(0, 0)
    # Setup registers 
    registerFrame = LabelFrame(root, padx = 0, pady = 0)
    registerFrame.grid(row = 0, column = 0)
    for i in range(number_of_regs):
        label_reg_name = setLabel(registerFrame, list_regs_string[i], anchor = W)
        label_reg_name.grid(row = i, column = 0, sticky = W)
        label = setLabel(registerFrame, regs_dict[list_regs[i]][1])
        label.grid(row = i, column = 4, sticky = E)
    updateStrVar()
    setRegsName()

    inputCommandFrame = LabelFrame(root, padx = 0, pady = 0)
    inputCommandFrame.grid(row = 0, column = 1) 
    commandLabel = Label(inputCommandFrame, text = 'Introduceti instructiunea', font = courier18)
    commandLabel.grid(row = 0, column = 1)
    inputCommand = Text(inputCommandFrame, height = 1, width = 25)
    inputCommand.grid(row = 1, column = 1) 
    sendCommand = Button(inputCommandFrame, text = 'Rulare Instructiune', command = lambda: runInstruction(inputCommand.get("1.0", END)))
    sendCommand.grid(row = 2, column = 1)
    
    # code to be emulated
    X86_CODE32 = b"\x41\x4a" # INC ecx; DEC edx
    
    # memory address where emulation starts
    ADDRESS = 0x1000000
    
    print("Emulate i386 code")
    try:
        # Initialize emulator in X86-32bit mode
        mu = Uc(UC_ARCH_X86, UC_MODE_32)

        # map 2MB memory for this emulation
        mu.mem_map(ADDRESS, 2 * 1024 * 1024)

        # write machine code to be emulated to memory
        mu.mem_write(ADDRESS, X86_CODE32)

        input('Press any key to continue')

        # initialize machine registers
        initializeRegisters(mu, registers_initial_values)
        readRegisters(mu)
        updateStrVar()

        input('Press any key to continue')
        # emulate code in infinite time & unlimited instructions
        mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE32))

        # now print out some registers
        # print("Emulation done. Below is the CPU context")
        
        
        readRegisters(mu)
        updateStrVar()
        printRegString()

    
    except UcError as e:
        print("ERROR: %s" % e)
    
    root.mainloop()