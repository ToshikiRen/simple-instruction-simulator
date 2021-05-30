
# Implementation details

## Millstones

- Setting up the unicorn-keystone-tkinter environment 
    - Problems:
        - Combining keystone and unicorn for easy assembling and testing of asm code 
- Adding memory viewing interface
    - Problems:
        - formating the memory in such a way that the user could read the data was a challenge at first
        - aligning memory cells 
        - adding hexll format to the memory while keeping the structure mostly the same
- Step by step running mode
    - Problems:
        - Memory:
            - This was by far the most challenging part of the project, after I added this functionality I had problems with the regular running mode while displaying the memory because it tried to update at each memory acces and it. 
            - To solve this problem I choose to update the memory only while doing step by step simulation and just add a button for memory updates that the user can click and instantly update the memory.
        - Step by step Highlight:
            - It was hard at first to think of a way to map each line of code to a memory address as keystone doesn't provide a memory address instruction mapping
            - To create this mapping I had to assemble each line of code on its own and create the memory mapping in this way. After I had the memory - instruction map it was easy to map the program lines to the memory and after that highlight the lines 