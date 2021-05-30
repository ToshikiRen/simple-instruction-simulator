# SMP-2021


## Project Objective:
Simulation of assembly instructions on a x86 32bit architecture with a easy to use user interface.
## Functionalities:
- General purpose register easy access in the main pannel of the simulator
- Running x86 32bit assembly code
    - step by step 
    - entire asm code at once 
- Memory view: hexll and side by side view (It allows the user to easily read the memory contents)
- syntax highlighting for the ISA (PS: for more instruction highlighting just edit the ISA.txt file with the instructions you want to be highlighted)



## Core Modules:
- [Unicorn](https://www.unicorn-engine.org/)
- [Keystone](https://www.keystone-engine.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

## Installation:

Be sure you have Python installed, then run the following commands in order to install the core modules used in this project: </br>
```
   pip install unicorn   - for UNICORN engine 
   pip install keystone  - for KEYSTONE engine
   pip install tk        - for GUI engine
```
You may need to install aditional modules needed by the core modules mentioned above.
# The SIMULATOR

The main pannel:
![image](images\Simulator_Base_View.png)

Step Simulation Example
![image](images\Simulator_Step_View.png)

Hexll Memory Format
![image](images\Simulator_Hexll_Memory_View.png)

## Similar projects:
1. [Carlosrafaelgn’s simulator](https://carlosrafaelgn.com.br/asm86/) - allows the simulation of x86 assembly instructions, easy registers and flags values access. The code runs without letting the user do a step by step simulation.
2. [Davis simulator](https://kobzol.github.io/davis/) - allows the simulation of an entire assembly program along with a nice registers values viewing interface, flags, RAM memory and the posibility to view memory by blocks of 1, 2 or even 4 bytes.
3. [Schweigi’s simulator](https://schweigi.github.io/assembler-simulator/) - an 8 bit simulator, with a reduced number of general purpose registers, but it offers the user the posibility to run instructions step-by-step along with step highlighting.
4. [Marss simulator](https://github.com/avadhpatel/marss)



For bug reports please feel free to email me at: necula.leonard.gabriel@gmail.com




