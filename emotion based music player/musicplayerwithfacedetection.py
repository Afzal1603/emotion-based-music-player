import tkinter as tk
import fnmatch
import os
from pygame import mixer
import cv2
from deepface import DeepFace
import tkinter.ttk as ttk

global emotion
canvas=tk.Tk()
canvas.title("Music Player")
canvas.geometry("600x600")
canvas.config(bg='black')

pattern="*.mp3"

mixer.init()
prevImg=tk.PhotoImage(file="prev_img.png")
stopImg=tk.PhotoImage(file="stop_img.png")
playImg=tk.PhotoImage(file="play_img.png")
pauseImg=tk.PhotoImage(file="pause_img.png")
nextImg=tk.PhotoImage(file="next_img.png")
faceImg=tk.PhotoImage(file="cropped-face.png")

def face():
    listBox.delete(0,'end')
    i=0
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces= faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            try:
                result = DeepFace.analyze(frame , actions=['emotion'])
                print(result[0]['dominant_emotion'])
                font = cv2.FONT_HERSHEY_SIMPLEX
                emotion=result[0]['dominant_emotion']
                cv2.putText(frame,result[0]['dominant_emotion'],
                   (50,50),font,1,(0,0,255),2,cv2.LINE_4)
                cv2.imshow('dummy video',frame)

            except:
                print("no")
        if(cv2.waitKey(2) & i==20):
            break
        i=i+1

    cap.release()
    cv2.destroyAllWindows()
    global rootpath

    if(emotion=="happy"):
        rootpath="F:\Final Project\Music\Happy"
    elif(emotion=="neutral"):
        rootpath="F:\\Final Project\Music\_Neutral"
    elif(emotion=="sad"):
        rootpath="F:\Final Project\Music\Sad"
    elif(emotion=="angry"):
        rootpath="F:\Final Project\Music\Angry"
    else:
        rootpath="F:\Final Project\Music\Surprise"
    for roots ,dirs ,files in os.walk(rootpath):
        for filename in fnmatch.filter(files,pattern):
            listBox.insert('end',filename)
    
def select():
        label.config(text=listBox.get("anchor"))
        mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
        mixer.music.play()    

def stop():
    mixer.music.stop()
    listBox.select_clear('active')

def next():
    nextSong=listBox.curselection()
    nextSong= nextSong[0]+1
    nextSongName=listBox.get(nextSong)
    label.config(text=nextSongName)

    mixer.music.load(rootpath + "\\" + nextSongName)
    mixer.music.play()

    listBox.select_clear(0,'end')
    listBox.activate(nextSong)
    listBox.select_set(nextSong)


def prev():
    nextSong=listBox.curselection()
    nextSong= nextSong[0]-1
    nextSongName=listBox.get(nextSong)
    label.config(text=nextSongName)

    mixer.music.load(rootpath + "\\" + nextSongName)
    mixer.music.play()

    listBox.select_clear(0,'end')
    listBox.activate(nextSong)
    listBox.select_set(nextSong)
def pause():
    if pauseButton["text"]=="Pause":
        mixer.music.pause()
        pauseButton["text"]="Play"
    else:
        mixer.music.unpause()
        pauseButton["text"]="Pause"

listBox=tk.Listbox(canvas,fg="cyan",bg="black",width=100,font=("pacifio",14))
listBox.pack(padx=15,pady=15)

label = tk.Label(canvas,text='',bg='black',fg='yellow',font=("pacifio",18))
label.pack(pady=15) 

top = tk.Frame(canvas,bg="black")
top.pack(padx=10,pady=5,anchor='center')


prevButton = tk.Button(canvas,text="Prev",image=prevImg,bg='black',borderwidth=0,command=prev)
prevButton.pack(pady=15,in_ = top, side = 'left')

stopButton = tk.Button(canvas,text="Stop",image=stopImg,bg='black',borderwidth=0, command=stop)
stopButton.pack(pady=15,in_ = top, side = 'left')

playButton = tk.Button(canvas,text="play",image=playImg,bg='black',borderwidth=0,command=select)
playButton.pack(pady=15,in_ = top, side = 'left')

pauseButton = tk.Button(canvas,text="pause",image=pauseImg,bg='black',borderwidth=0,command=pause)
pauseButton.pack(pady=15,in_ = top, side = 'left')

nextButton = tk.Button(canvas,text="next",image=nextImg,bg='black',borderwidth=0 ,command=next)
nextButton.pack(pady=15,in_ = top, side = 'left')

detectionButton = tk.Button(canvas,text="Detect",image=faceImg,bg='white',borderwidth=0,command=face)
detectionButton.pack(padx=180,pady=20)


canvas.mainloop()
