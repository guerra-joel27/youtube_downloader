import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import yt_dlp


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x350")

        ttk.Label(root, text="YouTube Downloader", font=("Arial", 16)).pack(pady=20)

        ttk.Label(root, text="Video URL:").pack()
