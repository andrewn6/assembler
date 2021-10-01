from tkinter import * 
from tkinter import filedialog
import tkinter as tk

import re
import sys
import os.path
filename = "Untitled"
filexxists = False

frame = tk.Tk()

def asmtoint(asm):
    import re
    asm_split = re.split(" |, |\(|\)", asm)
    args = []
    for i in range (len(asm_split)):
        if (asm_split[i] != ""):
            args.append(asm_split[i])
    opcode = 0
    func = 0
    rd = 0
    rs = 0
    rt = 0
    imm = 0
    if (args[0] == "sll"):
        if (len(args) !=4):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        func = 0
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "add"):
        if (len(args) !=4):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        func = 1
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "sub"):
        if (len(args) != 4):
            return 0, 0, 0, 0, 0, 0
        opcode = 0
        func = 2
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "nand"):
        if (len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 0
        func = 3
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "nor"):
        if (len(args) !=4):
            return 0,0,0,0,0,0
        opcode = 0
        func = 4
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
    elif (args[0] == "bez"):
        if (len(args) !=3):
            return 0,0,0,0,0,0
        opcode = 1
        rd = int(args[1][1:])
        rs = int(args[2][1:])
        rt = int(args[3][1:])
        imm = int(args[2])
    elif (args[0] == "bnez"):
        if (len(args) !=3):
            return 0,0,0,0,0,0
        opcode = 0
        rs = int(args[2][1:])
        rt = int(args[3][1:])
        imm = int(args[2])
    elif (args[0] == "bgez"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 1
        rt = 2
        rs = int(args[1][1:])
        imm = int(args[2])
    elif (args[0] == "bgz"):
        if (len(args) != 3):
            return 0,0,0,0,0,0
        opcode = 1
        rt = 4
        rs = int(args[1][1:])
        imm = int(args[2])
    elif (args[0] == "lw"):
        if (args[-1] == ''):
            args = args[0:-1]
        if (len(args) != 3 and len(args) !=4):
            return 0,0,0,0,0,0
        opcode = 2
        rt = int(args[1][1:])
        if (len(args) == 3):
            imm = 0
            rs = int(args[2][1:])
        else:
            imm = 0
            rs = int(args[3][1:])
    elif (args[0] == "sw"):
        if (args[-1] == ''):
            args = args[0:-1]
        if (len(args) != 3 and len(args) != 4):
            return 0,0,0,0,0,0
        opcode = 3
        rt = int(args[1][1:])
        if (len(args) == 3):
            imm = 0
            rs = int(args[2][1:])
        else:
            imm = int(args[2])
            rs = int(args[3][1:])
    else:
        return 0,0,0,0,0,0
    return opcode, rs, rt, rd, func, imm

def into_hex(opcode, rs, rt, rd, func, imm):
    if (opcode == 0):
        opstr = format(opcode, '02b')
        rsstr = format(rs, '03b')
        rtstr = format(rt, '03b')
        rdstr = format(rd, '03b')
        fnstr = format(func, '05b')
        ## print opstr, rsstr, rtstr, rdstr, fnstr <-- POC CODE
        instruc = opstr + rsstr + rtstr + rdstr + fnstr
    else:
        opstr = format(opcode, '02b')
        rtstr = format(rt, '03b')
        rsstr = format(rs, '03b')
        if (imm < 0):
            imm2s = ((-imm) ^ 255) + 1
            immstr = format(imm2s, '08b')
        else:
            immstr = format(imm, '08b')
        #print opstr, rtstr, rsstr, immstr <-- POC CODE
        instruc = opstr + rsstr + rtstr + immstr
    return format(int(instruc, 2), '04x')

def decode(asm):
    opcode, rs, rt, rd, func, imm = asmtoint(asm)
    instruc = into_hex(opcode, rs, rt, rs, func, imm)
    return instruc

def openFile():
    global filename
    openfilename = askopenfilename()
    if openfilename is not None:
        filename = openfilename
        asmfile = open(filename, "r")
        asmfile.seek(0)
        asmdata = asmfile.read()
        textArea.delete("1.0", "end - 1c")
        textArea.insert("1.0", asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = Normal)
        frame.title("Assembler [" + filename +"]")
        frame.focus()

def saveFile():
    global filename
    asmdata = textArea.get("1.0", "end - 1c")
    asmfile = open(filename, "w")
    asmfile.seek(0)
    asmfile.truncate()
    asmfile.write(asmdata)
    asmfile.close()

def saveFileAs():
    global filename
    global fileexists
    saveas_filename = asksaveasfilename()
    if saveas_filename is not None:
        filename = saveas_filename
        fileexists = True
        asmdata = textArea.get("1.0", "end - 1c")
        asmfile = open(filename, "w")
        asmfile.seek(0)
        asmfile.truncate()
        asmfile.write(asmdata)
        asmfile.close()
        filemenu.entryconfig(filemenu.index("Save"), state = Normal)
        frame.title("Assembler [" + filename +"]")
        frame.focus()

def exit_app():
    frame.destroy()
    sys.exit()


def compile_asm():
    global filename
    cpu_out = ""
    asm_in = textArea.get("1.0", END)
    asmlines = re.split("\n", asm_in)
    for i in range (len(asmlines)):
        if (asmlines[1] != ""):
            cpu_out += str(i) + " => x\"" + decode(asmlines[i]) + "\",\n"
    name, ext = os.path.splitext(filename)
    hexfilename = name + ".hex"
    hexfile = open(hexfilename, "w")
    hexfile.seek(0)
    hexfile.truncate()
    hexfile.write(cpu_out)
    hexfile.close()

tk().withdraw()
frame = TopLevel()

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
frame.title("Assembler ["+ filename + "]")
textArea = Text(frame, height=30, width=110, padx=2, pady=2, yscrollcommand = scrollbar.set)
textArea.pack(side=RIGHT)
scrollBar.config(command=textArea.yview)

menu = Menu(frame)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile, state = DISABLED)
filemenu.add_command(label="Save as...", command=saveFileAs)
filemenu.add_command(label="Exit", command=exitApp)
menubar.add_cascade(label="File", menu=filemenu)
runmenu = Menu(menubar, tearoff=0)
runmenu.add_command(label="Compile", command=compileASM)
menubar.add_cascade(label="Run", menu=runmenu)
frame.config(menu=menubar)

frame.minsize(750, 450)
frame.maxsize(750, 450)
frame.mainloop()