import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pytube
import threading
import os

def gui():
    def get_mp4():
        if not os.path.exists(path.get()):
            error_label.config(text='Invalid output directory!', fg='red')
            return
        error_label.config(text='Downloading MP4', fg='green')
        def download_mp4():
            try:
                link = ytEntry.get()
                yt = pytube.YouTube(link)
                selected_resolution = resolution_dropdown.get()
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_resolution).first()
                if stream:
                    stream.download(output_path=path.get())
                    error_label.config(text='Downloaded MP4!', fg='green')
                else:
                    error_label.config(text='Selected resolution not available!', fg='red')
            except pytube.exceptions.RegexMatchError:
                error_label.config(text='Invalid YouTube link!', fg='red')
            except Exception as e:
                error_label.config(text=f'Error: {str(e)}', fg='red')
        mp4_thread = threading.Thread(target=download_mp4)
        mp4_thread.start()

    def get_mp3():
        if not os.path.exists(path.get()):
            error_label.config(text='Invalid output directory!', fg='red')
            return
        error_label.config(text='Downloading MP3', fg='green')
        def download_mp3():
            error_label.config(text='Downloading MP3', fg='green')
            try:
                link = ytEntry.get()
                yt = pytube.YouTube(link)
                stream = yt.streams.filter(only_audio=True).first()
                stream.download(output_path=path.get(), filename=yt.title + '.mp3')
                error_label.config(text='Downloaded MP3!', fg='green')
            except pytube.exceptions.RegexMatchError:
                error_label.config(text='Invalid YouTube link!', fg='red')
            except Exception as e:
                error_label.config(text=f'Error: {str(e)}', fg='red')
        mp3_thread = threading.Thread(target=download_mp3)
        mp3_thread.start()

    def browse_directory():
        selected_directory = filedialog.askdirectory()
        path.delete(0, tk.END)
        path.insert(0, selected_directory)

    def update_resolutions(event):
        def update_res():
            link = ytEntry.get()
            if link:
                try:
                    yt = pytube.YouTube(link)
                    streams = yt.streams.filter(progressive=True, file_extension='mp4')
                    resolutions = list(set(stream.resolution for stream in streams))
                    resolutions.sort(reverse=True)
                    resolution_dropdown['values'] = resolutions
                    if resolutions:
                        resolution_dropdown.current(0)
                except pytube.exceptions.RegexMatchError:
                    error_label.config(text='Invalid YouTube link!', fg='red')
                except Exception as e:
                    error_label.config(text=f'Error: {str(e)}', fg='red')
            else:
                resolution_dropdown['values'] = []
        res_thread = threading.Thread(target=update_res)
        res_thread.start()

    window = tk.Tk()
    window.title("JDownloader")
    window.geometry("450x450")
    window.resizable(False, False)
    window.configure(background='#292929')
    window.iconbitmap('assets/JDownloader.ico')

    label = tk.Label(window, text="Enter Youtube Link", font=('Arial', 14), fg='white', bg='#292929')
    label.pack(side='top', pady=(10, 0))
    ytEntry_var = tk.StringVar()
    ytEntry = tk.Entry(window, textvariable=ytEntry_var, font=('Arial', 14), width=35, bd=2, relief='groove')
    ytEntry.pack()
    ytEntry.bind("<KeyRelease>", update_resolutions)

    pathlabel = tk.Label(window, text="Output Directory", font=('Arial', 14), fg='white', bg='#292929')
    pathlabel.pack(pady=(10, 0))
    path_frame = tk.Frame(window, background='#292929')
    path = tk.Entry(path_frame, font=('Arial', 14), width=27, bd=2, relief='groove')
    path.pack(side='left')
    path_button = tk.Button(path_frame, text="Browse", font=('Arial', 14), command=browse_directory, bd=2, relief='groove')
    path_button.pack(side='right', padx=5)
    path_frame.pack(pady=0)

    resolutions_label = tk.Label(window, text="Select Resolution", font=('Arial', 14), fg='white', bg='#292929')
    resolutions_label.pack(pady=(10, 0))
    resolution_dropdown = ttk.Combobox(window)
    resolution_dropdown.pack()

    error_label = tk.Label(window, font=('Arial', 14), fg='red', bg='#292929')
    error_label.pack()

    mp4_button = tk.Button(window, text="Download MP4", font=('Arial', 16), command=get_mp4, bd=2, relief='groove')
    mp4_button.pack(padx=30, side='left', pady=0)

    mp3_button = tk.Button(window, text="Download MP3", font=('Arial', 16), command=get_mp3, bd=2, relief='groove')
    mp3_button.pack(padx=30, side='right', pady=0)

    window.mainloop()
gui()