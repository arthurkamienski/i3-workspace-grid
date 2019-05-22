#!/usr/bin/python3

import sys
import json as parser
import subprocess
import os

from tkinter import *

def getActive(workspaces):
    active = []

    for workspace in workspaces:
        active.append(int(workspace['num']))
    
    return active

def getWorkspaces():
    return parser.loads(subprocess.check_output(['i3-msg', '-t', 'get_workspaces']).decode('utf-8'))

def getFocused(workspaces):
    focused = None

    for workspace in workspaces:
        if workspace['focused']:
                focused = workspace['num']

    return focused

# move or change to workspace
def switch(curr, dest, mode, active):
    if mode == 'move':
        os.system('i3-msg move container to workspace' + str(dest))
        active.append(dest)

    if len(set(active) & set([3,6,7,8,9])) != 0 or dest in [1, 2, 4, 5]:
        os.system('i3-msg workspace ' + str(dest))
        curr = dest

    return curr

# get next workspace
def getNext(curr, move, active):
    nxt = curr

    if move == 'up':
        if curr-3 > 0:
            nxt = curr-3
    elif move == 'down':
        if curr+3 < 10:
            nxt = curr+3
    elif move == 'left':
        if curr not in [1, 4, 7]:
            nxt = curr-1
    elif move == 'right':
        if curr not in [3, 6, 9]:
            nxt = curr+1
    elif move == 'next':
        nxt = active[(active.index(curr)+1)%len(active)]

    return nxt

def displayImage(focused, active):
    size = 90

    if len(set(active) & set([3,6,7,8,9])) != 0:
        rect_size = size/3
    else:
        rect_size = size/2

    root = Tk()
    root.attributes('-type', 'dialog')
    root.wm_attributes("-alpha", 0.5)
    root.overrideredirect(1)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry("+%d+%d" % (screen_width/2 - size/2, screen_height/2 - size/2))

    frame = Frame(root)

    frame.columnconfigure(0,weight=1)
    frame.rowconfigure(0,weight=1)

    display = Canvas(frame, bd=0, width=size, height=size, highlightthickness=0)

    for w in active:
        x = (w-1)%3
        y = (w-1)//3
        display.create_rectangle(x*rect_size, y*rect_size, (x+1)*rect_size, (y+1)*rect_size, fill='gray', outline='')

    x = (focused-1)%3
    y = (focused-1)//3
    display.create_rectangle(x*rect_size, y*rect_size, (x+1)*rect_size, (y+1)*rect_size, fill='gray20', outline='')

    display.grid(row=0, sticky=W+E+N+S)

    frame.pack(fill=BOTH, expand=1)
    root.after(200, lambda: root.destroy())
    frame.mainloop()

def main():
    name, mode, move = sys.argv
    
    if mode != 'display':
        workspaces = getWorkspaces()

        focused = getFocused(workspaces)
        active = getActive(workspaces)

        try:
            focused = switch(focused, int(move), mode, active)
        except Exception as e:
            focused = switch(focused, getNext(int(focused), move, active), mode, active)

    workspaces = getWorkspaces()
    focused = getFocused(workspaces)
    active = getActive(workspaces)

    displayImage(focused, active)

if __name__ == '__main__':
    main()