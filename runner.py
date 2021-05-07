# Main program
from utils import *


if "__main__" == __name__:
    
   

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

    # Add instructions frame
    inputCommandFrame = LabelFrame(root, padx = 0, pady = 0)
    inputCommandFrame.grid(row = 0, column = 1) 
    commandLabel = Label(inputCommandFrame, text = 'Introduceti secventa de cod', font = courier18)
    commandLabel.grid(row = 0, column = 1)

    
    # Add instruction writting textbox
    inputCommand = Text(inputCommandFrame, height = 17, width = 40)
    scroll = ttk.Scrollbar(inputCommandFrame, orient = VERTICAL, command = inputCommand.yview)
    scroll.grid(row = 1, column = 2, sticky='nsew')
    inputCommand['yscrollcommand'] = scroll.set
    inputCommand.grid(row = 1, column = 1) 

    commandFrame = LabelFrame(inputCommandFrame, padx = 0, pady = 0)
    commandFrame.grid(row = 2, column = 1)

    sendCommand = Button(commandFrame, text = 'Ruleaza Cod ', command = lambda: runInstruction(inputCommand.get("1.0", END), mu, ADDRESS))
    sendCommand.grid(row = 0, column = 0)
    runOneInstr = Button(commandFrame, text = 'Step Instruction ', command = lambda: runInstruction(inputCommand.get("1.0", END), mu, ADDRESS))
    runOneInstr.grid(row = 0, column = 1)
    
    
    # Functions Frame: Memory access and special registers view
    functionFrame = LabelFrame(root, padx = 0, pady = 0)
    functionFrame.grid(row = 1, column = 0) 

    # Memory window opener
    openMemoryButton = Button(functionFrame, text = 'Memorie', command = lambda: openMemory(mu, ADDRESS, MEM_SIZE))
    openMemoryButton.grid(row = 0, column = 0)
    
    # Memory hexll window opener
    openMemoryHexllButton = Button(functionFrame, text = 'Memorie Hexll', command = lambda: openMemoryPureHexll(mu, ADDRESS, MEM_SIZE))
    openMemoryHexllButton.grid(row = 0, column = 1)

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
        mu.hook_add(UC_HOOK_CODE, hook_code)
        # write machine code to be emulated to memory
    
        # initialize machine registers
        initializeRegisters(mu, registers_initial_values)
        readRegisters(mu)
        updateStrVar()

        print("x")
    except UcError as e:
        print("ERROR: %s" % e)
    
    root.mainloop()