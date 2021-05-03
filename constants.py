from __future__ import print_function
from unicorn import *
from unicorn.x86_const import *
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont 
from keystone import *

root = Tk()

instr_code = -1

mem = ''
ADDRESS = 0x0001000
MEM_SIZE = 8 * 512

courier24 = tkFont.Font(family="Courier", size=24, weight="bold")
courier18 = tkFont.Font(family="Courier", size=18, weight="bold")
courier10 = tkFont.Font(family="Courier", size=10, weight="bold")

# Registers default values
EAX_data = '00 00 00 00'
EBX_data = '00 00 00 00'
ECX_data = '00 00 00 00'
EDX_data = '00 00 00 00'
ESI_data = '00 00 00 00'
EDI_data = '00 00 00 00'
ESP_data = '00 00 00 00'
EBP_data = '00 00 00 00'

# Interface regs containers
EAX_str = StringVar('')
EBX_str = StringVar('')
ECX_str = StringVar('')
EDX_str = StringVar('')
ESI_str = StringVar('')
EDI_str = StringVar('')
ESP_str = StringVar('')
EBP_str = StringVar('')

# Adressable regs 
regs_dict = {
    'EAX' :[EAX_data, EAX_str],
    'EBX' :[EBX_data, EBX_str],
    'ECX' :[ECX_data, ECX_str],
    'EDX' :[EDX_data, EDX_str],
    'ESI' :[ESI_data, ESI_str],
    'EDI' :[EDI_data, EDI_str],
    'ESP' :[ESP_data, ESP_str],
    'EBP' :[EBP_data, EBP_str]
}

number_of_regs = 8

list_regs =[ 'EAX',
             'EBX',
             'ECX',
             'EDX',
             'ESI',
             'EDI',
             'ESP',
             'EBP']

EAX_sname = StringVar('')
EBX_sname = StringVar('')
ECX_sname = StringVar('')
EDX_sname = StringVar('')
ESI_sname = StringVar('')
EDI_sname = StringVar('')
ESP_sname = StringVar('')
EBP_sname = StringVar('')
memStringVar = StringVar('')


list_regs_string =[ EAX_sname,
                    EBX_sname,
                    ECX_sname,
                    EDX_sname,
                    ESI_sname,
                    EDI_sname,
                    ESP_sname,
                    EBP_sname ]


list_regs_x86 = [UC_X86_REG_EAX,
                UC_X86_REG_EBX,
                UC_X86_REG_ECX,
                UC_X86_REG_EDX,
                UC_X86_REG_ESI,
                UC_X86_REG_EDI,
                UC_X86_REG_ESP,
                UC_X86_REG_EBP]


instruction_set_arch = {
    'inceax' : '\x40',
    'incebx' : '\x43',
    'incecx' : '\x41',
    'incedx' : '\x42',
    'incesi' : '\x46',
    'incedi' : '\x47',
    'incesp' : '\x44',
    'incebp' : '\x45',
    'deceax' : '\x48',
    'decebx' : '\x4b',
    'dececx' : '\x49',
    'decedx' : '\x4a',
    'decesi' : '\x4e',
    'decedi' : '\x4f',
    'decesp' : '\x4c',
    'decebp' : '\x4d'
    
}

registers_initial_values = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]


