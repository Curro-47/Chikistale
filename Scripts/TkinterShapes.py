from tkinter import *
from tkinter import font as tkFont
import threading
import time

screenSize = None
lineWidth = None

def Init(_screenSize, _lineWidth):
    global screenSize, lineWidth
    screenSize = _screenSize
    lineWidth = _lineWidth

def Square(parent, x, y, w, h, bg='black', lc='white', anchor=CENTER, place=True):
    line = Canvas(parent, bg=lc)
    if place: line.place(x=screenSize[0]*x, y=screenSize[1]*y, width = screenSize[0]*w, height = screenSize[1]*h, anchor=anchor)

    square = Canvas(parent, bg=bg)
    if place: square.place(x=screenSize[0]*x, y=screenSize[1]*y, width = screenSize[0]*w-lineWidth, height = screenSize[1]*h-lineWidth, anchor=anchor)
    
    return square, line

def FillSquare(parent, x, y, w, h, bg='white', anchor=CENTER, place=True):
    square = Frame(parent, bg=bg)
    if place: square.place(x=screenSize[0]*x, y=screenSize[1]*y, width = screenSize[0]*w, height = screenSize[1]*h, anchor=anchor)
    return square

def ImageSquare(parent, image, x, y, w, h=None, rh=None, offset=(0,0), relative=True, bg='black', anchor=CENTER, image_anchor=CENTER, place=True):
    if (rh!=None and relative): h = w/screenSize[1]*screenSize[0]*rh
    if (rh!=None and not relative): h = w

    square = Frame(parent, bg=bg)
    if (relative) and place: square.place(x=screenSize[0]*x, y=screenSize[1]*y, width = screenSize[0]*w, height = screenSize[1]*h, anchor=anchor)
    elif place: square.place(x=screenSize[0]*x, y=screenSize[1]*y, width = w, height = h, anchor=anchor)
    
    image = Label(square, image=image, bg='black')
    if (relative == True): image.place(x=offset[0]*w*screenSize[0], y=offset[1]*h*screenSize[1], anchor=image_anchor)
    else: image.place(x=offset[0]*w, y=offset[1]*h, anchor=image_anchor)
    return square, image

def ImageButton(parent, image, x, y, w, h=None, rh=None, offset=(0,0), anchor=CENTER, image_anchor=CENTER, place=True):
    if (rh!=None): h = w/screenSize[1]*screenSize[0]*rh

    frame = Frame(parent, padx=0, bg='black')
    if place: frame.place(x=screenSize[0]*x, y=screenSize[1]*y, width = w, height = h, anchor=anchor)

    button = Button(frame, image=image, bg='black')
    button.place(x=offset[0], y=offset[1], anchor=image_anchor)

def TextSquare(parent, text, x, y, size=12, bg='black', tc='white', anchor=CENTER, place=True):
    font = tkFont.nametofont("TkDefaultFont")
    font.configure(size=size)

    label = Label(parent, text=text, font=font, bg=bg, fg=tc)
    if place: label.place(x=screenSize[0]*x, y=screenSize[1]*y, anchor=anchor)
    return label

def Resize(object, w, h, subObject = None):
    stepSize = 0.01

    currentSize = [object.winfo_width()/screenSize[0], object.winfo_height()/screenSize[1]]
    def _thread():
        while currentSize[0] != w or currentSize[1] != h:
            # Calculate width
            if currentSize[0]+stepSize < w: currentSize[0] += stepSize
            elif currentSize[0]-stepSize > w: currentSize[0] -= stepSize
            else: currentSize[0] = w
            # Calculate height
            if currentSize[1]+stepSize < h: currentSize[1] += stepSize
            elif currentSize[1]-stepSize > h: currentSize[1] -= stepSize
            else: currentSize[1] = h

            SetSize(object, currentSize[0], currentSize[1], subObject)
            time.sleep(0.02)

    thread = threading.Thread(target=_thread, daemon=True)
    thread.start()
    return thread
    

def SetSize(object, w, h, subObject = None):
    if (subObject != None): subObject.place_configure(width=w*screenSize[0]-lineWidth, height=h*screenSize[1]-lineWidth)
    object.place_configure(width=w*screenSize[0], height=h*screenSize[1])