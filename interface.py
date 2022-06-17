from tkinter import *
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
from signal import SIGINT, SIGKILL, SIGTERM, raise_signal
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

video_name = "test1.mp4" #This is your video file path
#video_name = "test.mkv" #This is your video file path
video = imageio.get_reader(video_name)


restartFlag = [False]
startFlag   = [False]
def stream(label):
    for image in video.iter_data():
        img = Image.fromarray(image).resize((400, 400))
        frame_image = ImageTk.PhotoImage(img)
        label.config(image=frame_image)
        label.image = frame_image
        break
    
    while(startFlag[0] == False):
        time.sleep(1)
    while(True):
        restartFlag[0] = False
        for image in video.iter_data():
            start = time.time()
            #end = time.time()
            #while ((end - start) < 0.02):
            #    end = time.time()
            img = Image.fromarray(image).resize((400, 400))
            frame_image = ImageTk.PhotoImage(img)
            label.config(image=frame_image)
            label.image = frame_image

        top = Toplevel(root, height=600, width=800)
        top.geometry
        top.title("Result Screen")
        Label(top, text= "RESULTS\n", font=('Mistral 18 bold')).place(x=450,y=80)

        while(restartFlag[0] == False):
            time.sleep(1)


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

def getText(difference):
    text = "asdf"

    if(difference < 20):
        text = "Not focusing\n"  
    elif(difference >= 20 and difference < 40):
        text = "Focusing started\n"  
    elif(difference >= 40):
        text = "Entered zen mode\n"

    return text


def exitProgram():
    root.destroy()
    raise_signal(SIGTERM)

def restartProgram():
    restartFlag[0] = True
    
def startProgram():
    startFlag[0] = True

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
    startButton = Button(root, text = 'Start Video', bd = '15', command = startProgram)
    restartButton = Button(root, text = 'Restart Video', bd = '5', command = restartProgram)
    exitButton = Button(root, text = 'Exit Program', bd = '5', command = exitProgram)

    # Graph
    style.use('ggplot')
    fig = plt.figure(figsize=(14, 2), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim(0, 4000)
    line, = ax.plot(ys, xs, 'r')

    plotcanvas = FigureCanvasTkAgg(fig, root)

    # Text
    textLabel = Label(root, text=getText(0))
    textLabel.config(font =("Nunito", 40), background='#ffffff')

    ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys, 1), interval=20, blit=False)

    plotcanvas.get_tk_widget().grid (row = 0, columnspan = 4, pady=20)
    videoLabel.grid                 (row = 1, rowspan = 2, column = 0, padx=100, pady=100)
    textLabel.grid                  (row = 1, column = 1, columnspan=3)
    startButton.grid                (row = 2, column = 1)
    restartButton.grid              (row = 2, column = 2)
    exitButton.grid                 (row = 2, column = 3)

    """     
    videoLabel.pack(side = TOP, anchor=NW, )
    plotcanvas.get_tk_widget().pack(side = TOP, anchor=NE)
    startButton.pack(side = LEFT, expand = True)
    restartButton.pack(side = LEFT, expand = True)
    exitButton.pack(side = LEFT, expand = True)
    """

    root.mainloop()