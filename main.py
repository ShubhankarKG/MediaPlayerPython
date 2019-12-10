# Imports necessary
import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer


# Function Definitions
def open_file():
    global filename_path
    try:
        filename_path = filedialog.askopenfilename()
        playlist_add(filename_path)

        mixer.music.queue(filename_path)
    except:
        pass


def playlist_add(filename):
    global filename_path
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


def create_playlist():
    directory = filedialog.askdirectory()
    os.chdir(directory)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            file1 = os.path.basename(file)
            playlistbox.insert(END, file1)
            playlist.insert(0, file)


def help():
    tkinter.messagebox.showinfo('About Music Player', 'This is a music player built using Python Tkinter by \n 1. '
                                                      'Shubhankar Gupta \n 2. Harsimran Virk \n 3. Rishikesh Hirde \n '
                                                      '4. Abhishek Kekane \n 5. Jash Seta')


def delete():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


def details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_label['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=count, args=(total_length,))
    t1.start()


def count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttime_label['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please check again.')


def pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def stop():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


def rewind():
    play()
    statusbar['text'] = "Music Rewinded"


def mute():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volume_btn.configure(image=volume_photo)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volume_btn.configure(image=mute_photo)
        scale.set(0)
        muted = TRUE


def quit():
    stop()
    root.destroy()


def next():
    try:
        stop()
        time.sleep(1)
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        play_it = playlist[selected_song+1]
        mixer.music.load(play_it)
        mixer.music.play()
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
        details(play_it)
    except :
        tkinter.messagebox.showerror('File not found', 'Music Player could not find the file. Please check again.')


root = tk.ThemedTk()
root.get_themes()  # Returns a list of all themes that can be set
root.set_theme("clearlooks")  # Sets an available theme

statusbar = ttk.Label(root, text="Welcome to Music Player", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=create_playlist)
subMenu.add_command(label="Exit", command=root.destroy)
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=help)

mixer.init()  # initializing the mixer

root.title("Music Player")
root.iconbitmap(r'images/musicplayer.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

frame_ListBox = Frame(root)
frame_ListBox.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(frame_ListBox)
playlistbox.pack()

add_btn = ttk.Button(frame_ListBox, text="+ Add", command=open_file)
add_btn.pack(side=LEFT)

del_btn = ttk.Button(frame_ListBox, text="- Del", command=delete)
del_btn.pack(side=LEFT)

frame_holder = Frame(root)
frame_holder.pack(pady=30)

frame_labelText = Frame(frame_holder)
frame_labelText.pack()

length_label = ttk.Label(frame_labelText, text='Total Length : --:--')
length_label.pack(pady=5)

currenttime_label = ttk.Label(frame_labelText, text='Current Time : --:--', relief=GROOVE)
currenttime_label.pack()

paused = FALSE
muted = FALSE


middleframe = Frame(frame_holder)
middleframe.pack(pady=30, padx=30)

play_photo = PhotoImage(file='images/play.png')
play_btn = ttk.Button(middleframe, image=play_photo, command=play)
play_btn.grid(row=0, column=0, padx=10)

stop_photo = PhotoImage(file='images/stop.png')
stop_btn = ttk.Button(middleframe, image=stop_photo, command=stop)
stop_btn.grid(row=0, column=1, padx=10)

pause_photo = PhotoImage(file='images/pause.png')
pause_btn = ttk.Button(middleframe, image=pause_photo, command=pause)
pause_btn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

frame_musicUtility = Frame(frame_holder)
frame_musicUtility.pack()

rewind_photo = PhotoImage(file='images/rewind.png')
rewind_btn = ttk.Button(frame_musicUtility, image=rewind_photo, command=rewind)
rewind_btn.grid(row=0, column=0)

mute_photo = PhotoImage(file='images/mute.png')
volume_photo = PhotoImage(file='images/volume.png')
volume_btn = ttk.Button(frame_musicUtility, image=volume_photo, command=mute)
volume_btn.grid(row=0, column=1)

next_photo = PhotoImage(file='images/next.png')
next_btn = ttk.Button(frame_musicUtility, image=next_photo, command=next)
next_btn.grid(row=0, column=2)

scale = ttk.Scale(frame_musicUtility, from_=0, to=100, orient=HORIZONTAL, command=lambda x : mixer.music.set_volume(float(x)/100))
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=3, pady=15, padx=30)

root.protocol("WM_DELETE_WINDOW", quit)
root.mainloop()
