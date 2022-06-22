from tkinter import *
from tkinter.tix import Tree
from turtle import back, color
from typing import ForwardRef
import imageio
from PIL import Image, ImageTk
import time
from threading import Thread
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from signal import SIGTERM, raise_signal

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

video_name = "test1.mp4" #This is your video file path
#video_name = "test.mkv" #This is your video file path
video = imageio.get_reader(video_name)


stopFlag  = [False]
startFlag = [False]
focusFlag = [False] 
def stream(label):
    focusDuration   = 0
    unfocusDuration = 0

    for image in video.iter_data():
        img = Image.fromarray(image).resize((800, 700))
        frame_image = ImageTk.PhotoImage(img)
        label.config(image=frame_image)
        label.image = frame_image
        break
    
    while(startFlag[0] == False):
        time.sleep(1)

    
    while(True):
        for image in video.iter_data():
            if(stopFlag[0] == True):
                time.sleep(1)
                continue

            if(focusFlag[0] == True):
                focusDuration += 0.03

                focusStatus.config(text="    Focusing")     
                focusResult.config(text="    %d second\n" % (focusDuration))     

            if(focusFlag[0] == False):
                unfocusDuration += 0.03

                focusStatus.config(text="    Not Focusing")     
                unfocusResult.config(text="    %d second\n" % (unfocusDuration))     


            #end = time.time()
            #while ((end - start) < 0.02):
            #    end = time.time()
            img = Image.fromarray(image).resize((800, 700))
            frame_image = ImageTk.PhotoImage(img)
            label.config(image=frame_image)
            label.image = frame_image



# Graph
xs = []
ys = []

def animate(i, xs, ys, data):
    # Add x and y to lists
    xs.append(i)
    ys.append(0)

    # Limit x and y lists to 20 items
    xs = xs[-200:]
    ys = ys[-200:]

    # Draw x and y lists
    #ax.clear()
    #ax.plot(xs, ys)

    line.set_data(xs, ys)
    ax.set_xlim(i-200, i)

    # Format plot
    plt.title('Frame Index')
    plt.ylabel('Signal Volume')



def exitProgram():
    root.destroy()
    raise_signal(SIGTERM)

def stopProgram():
    stopFlag[0] = True
    
def startProgram():
    startFlag[0] = True
    stopFlag[0] = False

def switchFocusProgram():
    if(focusFlag[0] == True):
        focusStatus.config(text = "    Not Focusing", foreground="#d9023b")
        focusFlag[0] = False
    elif(focusFlag[0] == False):
        focusStatus.config(text = "    Focusing", foreground='#23d100')
        focusFlag[0] = True

if __name__ == "__main__":
    # Main Frame
    root = Tk()
    root.geometry("1920x1080")
    #root.attributes('-fullscreen', True)
    root.title('Genero - Attention Test')
    root.state()
    root.config(background='#ffffff')
    # Video label
    videoLabel = Label(root)
    videoThread = Thread(target=stream, args=(videoLabel,))
    videoThread.daemon = 1
    videoThread.start()
    # Buttons
    buttonFrame = Frame(root, background='#ffffff')

    startButton = Button(buttonFrame, text = 'Start Video', bd = '5', command = startProgram, width = 30, height = 5)
    restartButton = Button(buttonFrame, text = 'Stop Video', bd = '5', command = stopProgram, width= 30, height= 5)
    exitButton = Button(buttonFrame, text = 'Exit Program', bd = '5', command = exitProgram, width= 30, height= 5)
    emptyButtonRow1 = Label(buttonFrame, text = "\n\n\n\n", background='#ffffff')
    emptyButtonRow2 = Label(buttonFrame, text = "\n\n\n\n", background='#ffffff')

    switchButton = Button(buttonFrame, text = 'Switch Focus', bd = '5', command = switchFocusProgram, width=30, height= 5)

    startButton.pack(side='top', expand=True)
    emptyButtonRow1.pack(side='top', expand=True)
    restartButton.pack(side='top', expand=True)
    emptyButtonRow2.pack(side='top', expand=True)
    exitButton.pack(side='top', expand=True)
    switchButton.pack(side='top', expand=True)


    # Graph
    style.use('ggplot')
    fig = plt.figure(figsize=(18, 2), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim(0, 4000)
    line, = ax.plot(ys, xs, 'r')

    plotcanvas = FigureCanvasTkAgg(fig, root)

    # Text
    textFrame = Frame(root, background='#ffffff')

    currentFocusStatus = Label(textFrame, text = "\n    Current Focus Status\n    -----------------------------")
    currentFocusStatus.config(font =("Nunito", 30), background='#ffffff', foreground='#000ac7')

    focusStatus = Label(textFrame, text = "    Not Focusing")
    focusStatus.config(font =("Nunito", 25), background='#ffffff', foreground='#d9023b')

    resultText = Label(textFrame, text = "\n    - Results - \n")
    resultText.config(font =("Nunito", 30), background='#ffffff', foreground='#000ac7')

    totalFocusLabel = Label(textFrame, text = "    Total Focused Time\n    -------------------------", foreground='#23d100')
    totalFocusLabel.config(font =("Nunito", 20), background='#ffffff')

    totalUnfocusLabel = Label(textFrame, text = "    Total Unfocused Time\n    -----------------------------", foreground='#d9023b')
    totalUnfocusLabel.config(font =("Nunito", 20), background='#ffffff')

    focusResult = Label(textFrame, text = "    0 second\n")
    focusResult.config(font =("Nunito", 20), background='#ffffff')

    unfocusResult = Label(textFrame, text = "    0 second\n")
    unfocusResult.config(font =("Nunito", 20), background='#ffffff')

    accuracyLabel = Label(textFrame, text = '\n    Accuracy Table\n    ---------------------')
    accuracyLabel.config(font =("Nunito", 20), background='#ffffff', foreground='#000ac7')

    focusPercentage = Label(textFrame, text = "    Focus Accuracy      : %0")
    focusPercentage.config(font =("Nunito", 20), background='#ffffff', foreground='#23d100')

    unfocusPercentage = Label(textFrame, text = "    Unfocus Accuracy  : %0")
    unfocusPercentage.config(font =("Nunito", 20), background='#ffffff', foreground='#d9023b')


    currentFocusStatus.pack(side='top')
    focusStatus.pack(side='top')
    accuracyLabel.pack(side='top')
    focusPercentage.pack(side='top')
    unfocusPercentage.pack(side='top')
    resultText.pack(side='top')
    totalFocusLabel.pack(side='top')
    focusResult.pack(side='top')
    totalUnfocusLabel.pack(side='top')
    unfocusResult.pack(side='top')

    ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys, 1), interval=20, blit=False)

    plotcanvas.get_tk_widget().grid (row = 0, columnspan = 6, pady=50)
    videoLabel.grid                 (row = 1, rowspan = 1, column = 1, columnspan=1, pady = 20)
    buttonFrame.grid                (row = 1, rowspan = 1, column = 0, columnspan=1, padx = 120)
    textFrame.grid                  (row = 1, rowspan = 1, column = 2, columnspan=1)


    def setFocus(difference):
        if(difference > 100):
            focusStatus.config("    Focusing")
        else:
            focusStatus.config("    Not Focusing")



    #currentFocusStatus.grid         (row=3, column=9)

    """     
    videoLabel.pack(side = TOP, anchor=NW, )
    plotcanvas.get_tk_widget().pack(side = TOP, anchor=NE)
    startButton.pack(side = LEFT, expand = True)
    restartButton.pack(side = LEFT, expand = True)
    exitButton.pack(side = LEFT, expand = True)
    """

    root.mainloop()