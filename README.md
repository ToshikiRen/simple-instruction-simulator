# SMP-2021


## Project Objective:
Integration of simulation and assembly instruction generator on a x86 32bit architecture with a easy to use user interface.
## Functionalities:
- General purpose register easy access
- Running x86 32bit assembly code  
- Memory view: hexll and side by side view
## Similar projects:
1. [Carlosrafaelgn’s simulator](https://carlosrafaelgn.com.br/asm86/) - allows the simulation of x86 assembly instructions, easy registers and flags values access. The code runs without letting the user do a step by step simulation.
2. [Davis simulator](https://kobzol.github.io/davis/) - allows the simulation of an entire assembly program along with a nice registers values viewing interface, flags, RAM memory and the posibility to view memory by blocks of 1, 2 or even 4 bytes.
3. [Schweigi’s simulator](https://schweigi.github.io/assembler-simulator/) - an 8 bit simulator, with a reduced number of general purpose registers, but it offers the user the posibility to run instructions step-by-step along with step highlighting.
4. [Marss simulator](https://github.com/avadhpatel/marss)



## Base Modules:
- [Unicorn](https://www.unicorn-engine.org/)
- [Keystone](https://www.keystone-engine.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

## Instalation:

Run the following commands in order to install the core modules used in this project: </br>
```
   pip install unicorn   - for UNICORN engine 
   pip install keystone  - for KEYSTONE engine
   pip install tk        - for GUI engine
```


For bug reports please feel free to email me at: necula.leonard.gabriel@gmail.com




