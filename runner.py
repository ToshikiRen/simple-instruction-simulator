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
    inputCommand = Text(inputCommandFrame, height = 10, width = 40)
    inputCommand.grid(row = 1, column = 1) 
    sendCommand = Button(inputCommandFrame, text = 'Rulare Instructiune', command = lambda: runInstruction(inputCommand.get("1.0", END), mu, ADDRESS))
    sendCommand.grid(row = 2, column = 1)
    
    openMemoryButton = Button(root, text = 'Memorie', command = lambda: openMemory(mu, ADDRESS, MEM_SIZE))
    openMemoryButton.grid(row = 3, column = 0)
    

    # code to be emulated
    X86_CODE32 = b"\x41\x4a" # INC ecx; DEC edx
    
    # memory address where emulation starts

    print("Emulate i386 code")
    try:
        # Initialize emulator in X86-32bit mode
        mu = Uc(UC_ARCH_X86, UC_MODE_32)

        # map memory for this emulation
        mu.mem_map(ADDRESS, MEM_SIZE)

        # adding code running hook
        mu.hook_add(UC_HOOK_MEM_WRITE, hook_mem)
        # write machine code to be emulated to memory
    
        # initialize machine registers
        initializeRegisters(mu, registers_initial_values)
        readRegisters(mu)
        updateStrVar()
    
    except UcError as e:
        print("ERROR: %s" % e)
    
    root.mainloop()