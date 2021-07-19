from __future__ import unicode_literals
import os
import youtube_dl
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog

'''
If there are any errors while downloading, you may try running 'youtube-dl --rm-cache-dir'
'''

def YT_downloader():
    global path, option
    
    url = url_input.get()
    if url == '':
        create_error_window('\"Youtube site" is unfilled')
        return None
    
    save_path = path.get()
    if save_path == '':
        create_error_window('No destination folder is selected')
        return None
    
    name = download_name_input.get()
    if name == '':
        create_error_window('\"Output file path\" is unfilled')
        return None
    
    save_format = option.get()
    
    save_name = name + '.' + save_format
    tmp_path = os.path.join(save_path, save_name)
    
    if(os.path.isfile(tmp_path)):
        create_error_window('The current folder already contains\n a folder named ' + save_name)
        return None
    
    if save_format == 'wav':
        ydl_wav_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            }],
            'outtmpl': save_name
        }
        with youtube_dl.YoutubeDL(ydl_wav_opts) as ydl:
            ydl.download([url])
    else:
        ydl_mp4_opts = {
            'outtmpl': save_name
        }
        with youtube_dl.YoutubeDL(ydl_mp4_opts) as ydl:
            ydl.download([url])
    
    program_path = os.path.dirname(__file__)
    file_path = os.path.join(program_path, save_name)
    dir_path = os.path.join(save_path, save_name)
    os.rename(file_path, dir_path)
    return None

def create_error_window(error_msg):
    # build subwindow
    error_window = tk.Toplevel(window)
    error_window.title('Error')
    error_window.geometry('300x150')
    error_window.configure(background='white')
    
    # create image
    tk.Label(error_window, text='Error', font=('Times New Roman', 18), bg='#fff').pack()
    error_label = tk.Label(error_window, text=error_msg, font=('Times New Roman', 14), bg='#fff')
    
    # place image
    error_label.place(x=150, y=75, width=300, height=40, anchor='center')

def save_browse_event():
    global path
    filename = filedialog.askdirectory()
    path.set(filename)

def PlaceAll():
    title_label.place(x=250, y=0, width=400, height=40, anchor='n')
    
    upload_label.place(x=60, y=80, width=120, height=40)
    url_input.place(x=180, y=80, width=260, height=40)
    
    save_label.place(x=60, y=120, width=120, height=40)
    path_label.place(x=180, y=120, width=200, height=40)
    browse_save_button.place(x=380, y=120, width=60, height=40)
    download_name_label.place(x=60, y=160, width=120, height=40)
    download_name_input.place(x=180, y=160, width=260, height=40)
    
    format_label.place(x=60, y=200, width=120, height=40)
    menu.place(x=180, y=200, width=120, height=40)
    download_button.place(x=250, y=280, width=120, height=40, anchor='n')
    

if __name__ == '__main__':
    # parameters
    font = ('Times New Roman', 12)
    font_title = ('Times New Roman', 20)
    
    # build window
    window = tk.Tk()
    window.title('youtube downloader')
    window.geometry('500x350')
    window.configure(background='gray')
    
    # folder browse
    title_label = tk.Label(window, text='YOUTUBE DOWNLOADER', font=font_title)
    
    path = tk.StringVar()
    upload_label = tk.Label(window, text='Youtube site:', font=font)
    url_input = tk.Entry(font=font)
    
    save_label = tk.Label(window, text='Destination: ', font=font)
    path_label = tk.Label(window, textvariable=path, font=font, bg='#fff')
    browse_save_button = tk.Button(window, text='Browse', font=font, command=save_browse_event)
    download_name_label = tk.Label(window, text='Output file name: ', font=font)
    download_name_input = tk.Entry(window, font=font)
    
    option_list = ['mp4', 'wav']
    option = tk.StringVar()
    option.set(option_list[0])
    format_label = tk.Label(window, text='Format:', font=font)
    menu = tk.OptionMenu(window, option, *option_list)
    download_button = tk.Button(window, text='download', font=font, command=YT_downloader)
    
    PlaceAll();
    
    window.mainloop()