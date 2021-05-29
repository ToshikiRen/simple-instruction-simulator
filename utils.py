# Functions module
from constants import *





# TODO: (DONE)  Set labels
def setLabel(root, stringVar, font=courier24, anchor="e", justify=LEFT, padx=0,
             width=16):
    return Label(root, textvariable=stringVar, font=font, anchor=anchor,
                 justify=justify, padx=padx)

# TODO: (DONE)  Updates the values of the registers from the interface
def updateStrVar():

    for i in range(number_of_regs):
        regs_dict[list_regs[i]][1].set(regs_dict[list_regs[i]][0])
    
    
# TODO: (DONE)  Formats the register
def formatRegisterString(regString, regName):

    regString = regString.replace('0x', '')
    # returnString = regName + ': '
    returnString = ''
    reg_bytes = len(regString)
    nedded_header = '0' * (8 - reg_bytes)
    regString = nedded_header + regString

    # Groups the bits in blocks of 2 hexa
    for i in range(0, 4):
        returnString += regString[2*i: 2*i + 2]
        if i < 3:
            returnString += ' '

    return returnString

# TODO: (DONE)  Displays in the console the register values
def printRegString():

    for reg in list_regs:
        print(regs_dict[reg][0])


# TODO: (DONE)  Reads the registers values
def readRegisters(mu):

    for i in range(0, number_of_regs):
        regs_dict[list_regs[i]][0] = formatRegisterString(
            hex(mu.reg_read(list_regs_x86[i])), list_regs[i])
        regs_dict[list_regs[i]][0] = regs_dict[list_regs[i]][0].upper()

    # print( mu.reg_read(UC_X86_REG_EIP))
# TODO: (DONE)  Initialize registers
def initializeRegisters(mu, listOfValues):

    for i in range(number_of_regs):
        mu.reg_write(list_regs_x86[i], listOfValues[i])
    mu.reg_write(UC_X86_REG_EIP, ADDRESS)
# TODO: (DONE) Set registers names
def setRegsName():

    for i in range(number_of_regs):
        list_regs_string[i].set(list_regs[i] + ': ')

# TODO: (DONE)  Run instruction
def runInstruction_old(instr, mu, ADDRESS):

    global instr_code
    instr = instr.replace(" ", "")
    instr = instr.replace("\n", '')
    instr = instr.lower()
    
    try:
        # print(instr, end='\n')
        instr_code = instruction_set_arch[instr]
        # print(instr_code, end='\n')
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

# TODO: Get Instruction code
def getInstruction(instr, mu, ADDRESS):

    global instr_code

    # instance of Keystone
    try:
        # Setup a keystone object
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        #instr = instr.replace("\n", '')
        instr_code, count = ks.asm(instr)
        
        instr_address = [ADDRESS]
        idx = 0
        idx_list = []
        for line in instr.split("\n"):
        
            #print(line )
            idx += 1
            try:
                instr_mini_code, count_mini = ks.asm(line)
            except:
                last_instr = line.split(' ')
                #print(last_instr)
                last_instr = last_instr[-1]
                last_instr = last_instr.replace(';', '')
                print(line + ';' + '\n' + last_instr + ":")
                instr_mini_code, count_mini = ks.asm(line + ';' + '\n' + last_instr + ":")
            
            if instr_mini_code != None:
                if len(instr_mini_code) > 0: 
                    instr_address.append(instr_address[-1] + len(instr_mini_code))
                    idx_list.append(idx)

            
        for idx in range(len(idx_list)):
            local_addr = instr_address[idx]
            local_addr = "%04X"%local_addr
            EIP_line_number_dict[local_addr] = idx_list[idx]

        print(idx_list)
        print(instr_address)
        print(EIP_line_number_dict)
        print("Count is : {}".format(count))
        instr = bytes()

        for x in instr_code:
            instr = instr + bytes([x])
        instr_code = instr
    # Error handling
    except KsError as e:
        print("Error: %s", e)
        instr_code = -1
    
   


# TODO: (DONE)  Run an instruction at a give address
def runInstruction(instr, mu, ADDRESS, step = False):

    global instr_code, startStep, wasStep
    global Exp
    print(Exp.text)
    wasStep = step
    if not step or (step and startStep == 1):
        getInstruction(instr, mu, ADDRESS)
        startStep = 0
    # print(startStep)
    # Check if an error has occured
    if instr_code != -1:
        try:
            mu.mem_write(ADDRESS, instr_code)
        except:
            print("Memory write FAILED!!")

        if not step:
            runInstructionOn(mu, ADDRESS, instr_code)
            # read_mem_format(mu, ADDRESS, MEM_SIZE)
            instr_code = -1
            readRegisters(mu)
            updateStrVar()
            # printRegString()
        else:
            EIP_value = mu.reg_read(UC_X86_REG_EIP)
            line_nb = EIP_line_number_dict["%04X"%EIP_value]
            print(line_nb)
            Exp.text.tag_remove("line_step", 1.0, "end")
            Exp.text.tag_add("line_step", str(line_nb) + '.0', str(line_nb) + '.100')
            runOneInstruction(mu, ADDRESS, instr_code)
            readRegisters(mu)
            updateStrVar()

def hook_mem(uc, access, address, size, value, user_data):

    global wasStep
    if wasStep:
        mem, _ = read_mem_format(uc, ADDRESS, MEM_SIZE, pure_hexll = True)
        memPureHexllStringVar.set(mem)
        mem, _ = read_mem_format(uc, ADDRESS, MEM_SIZE, pure_hexll = False)
        memStringVar.set(mem)
    

def hook_code(uc, address, size, user_data):

    pass
    print("Hook call instr: ADDR: {} SIZE: {}".format(address, size))



# TODO: (DONE)  Convert to hex, but keeps double 00 intact
def my_hex(to_hex):

    return "%02X"%to_hex


# TODO: (DONE) Formats the adress range for display purposes
def add_address_range(start_address, per_row, max_len):

    frm = "%0" + str(max_len) + "X"
    end_addr = start_address
    end_addr += (per_row - 1)
    start = frm%start_address
    
    end = frm%end_addr

    # return start + '->' + end + ': '
    return start + ": "

# TODO: (DONE) Convert data to HEXLL format
def hexll(to_hexll, pure_hexll = False):

    if chr(to_hexll).isalpha():
        return "." + chr(to_hexll)
    elif not pure_hexll:
        return ". "    
    else:
        return my_hex(to_hexll)

# TODO: (DONE) Reads data from memory 
def read_mem_format(mu, start_address, quantity, per_row = 16, pure_hexll = False):

    mem = mu.mem_read(start_address, quantity)
    mem_data = ''
    max_len = len(str(start_address + quantity//16))
    for i in range(0, quantity//per_row):
        mem_data += add_address_range(start_address, per_row, max_len)
        start_address += per_row
        if not pure_hexll:
            mem_data += " ".join([my_hex(x)
                                for x in (mem[i * per_row: per_row * (i + 1)])])
            mem_data += "    "

            mem_data += " ".join([hexll(x)
                            for x in (mem[i * per_row: per_row * (i + 1)])])

        else:
            mem_row = " ".join([hexll(x, True)
                            for x in (mem[i * per_row: per_row * (i + 1)])])
            mem_data += mem_row
           

        mem_data += '\n'

    return mem_data, len(add_address_range(start_address, per_row, max_len))
    # for byte in reversed(mem):
    #    print(hex(byte), end = "")
    # print("")
    # print(mu.reg_read(UC_X86_REG_DS))


def setupUI():

    pass


def runInstructionOn(mu, address, instr_code):
    # TODO: Add count = number_of_instr_to_run
    mu.emu_start(address, address + len(instr_code))

def runOneInstruction(mu, address, instr_code):

    EIP_value = mu.reg_read(UC_X86_REG_EIP) 
    mu.emu_start(EIP_value, address + len(instr_code), count = 1)


# Tkinter

# TODO: (DONE)  Create a scrollable canvas inside a given frame
def createScrollableCanvas(main_frame, window = None, Ox = None, Oy = True):
    
    main_frame.pack(fill = BOTH, expand = 1)

    # Adding the canvas
    canvas = Canvas(main_frame)
    canvas.pack(side = LEFT, fill = BOTH, expand = 1)

    if Oy:
        # Adding the scrollbar
        scroll = tk.Scrollbar(main_frame, orient = VERTICAL, command = canvas.yview)
        scroll.pack(side = RIGHT, fill = Y)
        
        # Canvas configuration
        canvas.configure(yscrollcommand = scroll.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1 * (event.delta/120)), "units"))
    if Ox:
        if window:
            scrollX = tk.Scrollbar(window, orient = HORIZONTAL, command = canvas.xview)
        else:
            scrollX = tk.Scrollbar(main_frame, orient = HORIZONTAL, command = canvas.xview)
        scrollX.pack(side = BOTTOM, fill = X)
        
        # Canvas configuration
        canvas.configure(xscrollcommand = scrollX.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))


    
    # Secondary frame
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window = second_frame, anchor = "nw")

    return second_frame

# TODO: (DONE)  Scrollable window
def openWindow(title, size):

    newWindow = Toplevel(root)
    newWindow.geometry(size)
    newWindow.title(title)
    # newWindow.resizable(0, 0)
    # Create a frame for the canvas
    main_frame = Frame(newWindow)
    

    return newWindow, main_frame

# TODO: (DONE) Displays memory contents
def openMemory(mu, start_address=ADDRESS, quantity=MEM_SIZE, title="Memory", size="940x400"):

    global mem
    # Set up the window for memory display
    window, main_frame = openWindow(title, size)
    
    mem, offset = read_mem_format(mu, start_address, quantity)
    memStringVar.set(mem)


    stringVarData = offset * " " + " ".join(my_hex(index) for index in range(0, 16))
    memAddressString = StringVar('')
    memAddressString.set(stringVarData)
    stringAddressLabel = setLabel(main_frame, memAddressString, courier10, anchor="w", justify=LEFT)
    stringAddressLabel.pack(side = TOP, anchor = "w")

    windowFrame = createScrollableCanvas(main_frame, window, True, True)
    


    # print(offset)

    # Adds the update memory button
    updateMeme = Button(window, text = 'Update', command = lambda: updateMemory(mu, ADDRESS, MEM_SIZE))
    updateMeme.pack(side = BOTTOM) 
    label = setLabel(windowFrame, memStringVar, courier10, anchor="center", justify=LEFT, padx=0,
                     width=16)
    label.grid(row = 1, column = 0)

# TODO: (DONE) Updates memory display window
def updateMemory(mu, address, mem_size):

    mem, _ = read_mem_format(mu, address, mem_size)
    memStringVar.set(mem)



# TODO: (DONE) Displays memory contents hexll
def openMemoryPureHexll(mu, start_address=ADDRESS, quantity=MEM_SIZE, title="Memory Hexll", size="460x400"):

    global memPureHexllStringVar
    # Set up the window for memory display
    window, main_frame = openWindow(title, size)
    
    mem, offset = read_mem_format(mu, start_address, quantity, pure_hexll = True)
    memPureHexllStringVar.set(mem)


    stringVarData = offset * " " + " ".join(my_hex(index) for index in range(0, 16))
    memAddressString = StringVar('')
    memAddressString.set(stringVarData)
    stringAddressLabel = setLabel(main_frame, memAddressString, courier10, anchor="w", justify=LEFT)
    stringAddressLabel.pack(side = TOP, anchor = "w")

    windowFrame = createScrollableCanvas(main_frame, window, True, True)

    # print(mem)

    # Adds the update memory button
    updateMeme = Button(window, text = 'Update', command = lambda: updateMemoryHexll(mu, ADDRESS, MEM_SIZE))
    updateMeme.pack(side = BOTTOM) 
    label = setLabel(windowFrame, memPureHexllStringVar, courier10, anchor="center", justify=LEFT, padx=0,
                     width=16)
    label.grid(row = 1, column = 0)

# TODO: (DONE) Updates memory display window
def updateMemoryHexll(mu, address, mem_size):

    mem, _ = read_mem_format(mu, address, mem_size, pure_hexll = True)
    memPureHexllStringVar.set(mem)


# TODO: (DONE) Reset step
def resetStep(mu):

    global startStep
    startStep = 1
    mu.reg_write(UC_X86_REG_EIP, ADDRESS)
    Exp.text.tag_remove("line_step", 1.0, "end")
    initializeRegisters(mu, registers_initial_values)
    readRegisters(mu)
    updateStrVar()


# Line numbering classes

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget
        
    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, master, case_insensetive = True, current_line_colour = '', word_end_at = r""" .,{}[]()=+-*/\|<>%""", tags = {},  *args, **kwargs):
        
        tk.Text.__init__(self, master = master, *args, **kwargs)
        
        self.bind("<KeyRelease>", lambda e: self.highlight())
        
        self.case_insensetive = case_insensetive
        self.highlight_current_line = current_line_colour != ''
        self.word_end = word_end_at
        self.tags = tags
        
        if self.case_insensetive:
            for tag in self.tags:
                self.tags[tag]['words'] = [word.lower() for word in self.tags[tag]['words']]
        

        self.tag_config('line_step', background = 'blue')
        #loops through the syntax dictionary to creat tags for each type
        for tag in self.tags:
            self.tag_config(tag, **self.tags[tag]['style'])
        
        if self.highlight_current_line:
            self.tag_configure("current_line", background = current_line_colour)
            self.tag_add("current_line", "insert linestart", "insert lineend+1c")
            self.tag_raise("sel")

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)


        #find what is the last word thats being typed.
    def last_word(self):
        line, last = self.index(tk.INSERT).split('.')
        last=int(last)
        
        #this limit issues when user is a fast typer
        last_char = self.get(f'{line}.{int(last)-1}', f'{line}.{last}')
        while last_char in self.word_end and last > 0:
            last-=1          
            last_char = self.get(f'{line}.{int(last)-1}', f'{line}.{last}')
            
        first = int(last)
        while True:
            first-=1
            if first<0: break
            if self.get(f"{line}.{first}", f"{line}.{first+1}") in self.word_end:
                break
        return {'word': self.get(f"{line}.{first+1}", f"{line}.{last}"), 'first': f"{line}.{first+1}", 'last': f"{line}.{last}"}
    
    #highlight the last word if its a syntax, See: syntax dictionary on the top.
    #this runs on every key release which is why it fails when the user is too fast.
    #it also highlights the current line
    def highlight(self):
        
        if self.highlight_current_line:
            self.tag_remove("current_line", 1.0, "end")
            self.tag_add("current_line", "insert linestart", "insert lineend+1c")
        
        lastword = self.last_word()
        wrd = lastword['word'].lower() if self.case_insensetive else lastword['word']
        wrd = wrd.replace(" ", "") 
        wrd = wrd.replace("\t", "")
        for tag in self.tags:      
            if wrd in self.tags[tag]['words']:
                self.tag_add(tag, lastword['first'], lastword['last'])
            else:                  
                self.tag_remove(tag, lastword['first'], lastword['last'])
        
        self.tag_raise("sel")


    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        #result = self.tk.call(cmd)
        try:
            result = self.tk.call(cmd)
        except Exception:
            return ""
        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result      



class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        global syntax
        syntax = self.loadHighlight()
        self.text = CustomText(master = self,
            
            case_insensetive = True, #True by default.
            current_line_colour = 'grey10', #'' by default which will not highlight the current line.
            word_end_at = r""" .,{}[]()=+-*/\|<>%""", #<< by default, this will till the class where is word ending.
            tags = {#'SomeTagName': {'style': {'someStyle': 'someValue', ... etc}, 'words': ['word1', 'word2' ... etc]}} this tells it to apply this style to these words
                #"failSynonyms": {'style': {'foreground': 'red', 'font': 'helvetica 8'}, 'words': ['fail', 'bad']},
   
                "passSynonyms":{'style': {'foreground': '#00FF80', 'font': 'Courier 12'}, 'words': self.getRegsWithEndings()},
                "assemblySyntax":{'style': {'foreground': '#FF0040', 'font': 'Courier 12'}, 'words': syntax}
                
               
                },
            font='helvetica 12',   #Sandard tkinter text arguments
            background = 'BLACK',       #Sandard tkinter text arguments
            foreground = 'white',        #Sandard tkinter text arguments
            
            
            width = 45, height = 20)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.configure(insertbackground = 'blue')
        self.text.tag_configure("bigfont", font=courier18)

        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)
        
        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
       # self.text.bind("<KeyPress>", self._print_line)

        self.text.tag_config("start", background="blue")
        #self.text.tag_config("initial", background="blue")


        self.text.insert("end", "Introduceti secventa de cod\n",("bigfont",))
    
    def loadHighlight(self, file = 'ISA.txt'):
        
        f = open(file, mode = 'r')
        tags = []
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n", "")
            tags.append(line)
        f.close()
        return tags

    def getRegsWithEndings(self):
        
        global list_regs
        
        regs = list_regs
        regs += ['AH', 'AL', 'AX', 'BH', 'BX', 'BL', 'CH', 'CX', 'CL', 'DH', 'DX', 'DL']
        regList = []
        for reg in regs:
            regList.append(reg)
            regList.append(reg + ';')
        

        return regList

    def _print_line(self, event):
        # For enter event.keycode is equal to 12
        global lastLine
        currentLine = int(float(self.text.index(INSERT)))
        
        #if lastLine != currentLine:
        lastLineStr = str(lastLine)
        currentLineStr = str(currentLine)
        #for tag in self.text.tag_names():
        #    if tag == 'start':
        #        self.text.tag_delete(tag)
        print("Tag added on line " + currentLineStr)
        self.text.tag_add("start",  currentLineStr + '.0', currentLineStr + '.50')  
        #self.text.tag_add("start",  lastLineStr + '.0', lastLineStr + '.50')

        lastLine = currentLine

    def _on_change(self, event):
        self.linenumbers.redraw()
		

# Add instructions frame
inputCommandFrame = LabelFrame(root, padx = 0, pady = 0)
inputCommandFrame.grid(row = 0, column = 1) 
Exp = Example(inputCommandFrame)
Exp.grid(row = 0, column = 1)