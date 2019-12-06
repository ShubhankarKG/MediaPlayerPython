from tkinter import *
import tkinter.filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading


if __name__ == "__main__":
    isPaused = False
    file_name = ""

    def play_music():
        global isPaused
        global song_len
        if isPaused:
            isPaused = False
            mixer.music.unpause()
        else:
            if file_name == "":
                song_name["text"] = "test.mp3"
                mixer.music.load("test.mp3")
                mixer.music.play()
            else:
                mixer.music.load(file_name)
                mixer.music.play()
                thread = threading.Thread(target=timer, args=(song_len,))
                thread.start()

    def pause_music():
        global isPaused
        if isPaused is False:
            isPaused = True
        mixer.music.pause()

    def vol_control(vol):
        volume = float(vol)/100
        mixer.music.set_volume(volume)

    def search_file():
        global file_name
        global song_len
        file_name = tkinter.filedialog.askopenfilename()
        song_name['text'] = file_name.split('/')[-1] #Works for linux and mac, but not for Windows
        song_len = MP3(file_name).info.length
        total_time["text"] = time.strftime("%M:%S", time.gmtime(song_len))
        #timer(song_len)
        if mixer.music.get_busy():
            mixer.music.stop()

    def timer(length):
        while(length):
            current_time["text"] = time.strftime("%M:%S", time.gmtime(length))
            length -= 1
            time.sleep(1)

    # BASIC TKINTER CODE
    m1 = PanedWindow()
    mixer.init()
    m1.pack(fill=BOTH, expand=1)
    frame = LabelFrame(m1, bd=5)
    m1.add(frame)
    song_name = Message(frame, width=300)
    song_name.grid(row=0,columnspan=2)
    total_time = Label(frame, width=20)
    total_time.grid(row=1, column=0)
    current_time = Label(frame,width=20)
    current_time.grid(row=1, column=1)
    m2 = PanedWindow(m1, orient=VERTICAL)
    m1.add(m2)
    top = Scale(m2, orient=HORIZONTAL, command=vol_control)
    top.set(100)
    m2.add(top)
    play = Button(m2, text="Play", command=play_music)
    m2.add(play)
    pause = Button(m2, text="Pause", command=pause_music)
    m2.add(pause)
    search = Button(m2, text="Search", command=search_file)
    m2.add(search)
    mainloop()
