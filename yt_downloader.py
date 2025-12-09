import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import yt_dlp


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x400")

        ttk.Label(root, text="YouTube Downloader", font=("Arial", 16)).pack(pady=20)

        ttk.Label(root, text="Video URL:").pack()
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        ttk.Label(root, text="Download Type:").pack(pady=(10, 0))
        self.download_type = tk.StringVar(value="Video (Best)")
        ttk.Combobox(
            root,
            textvariable=self.download_type,
            values=["Videos (Best)", "Video Only (720)", "Audio Only"],
            state="readonly",
            width=20,
        ).pack()

        ttk.Label(root, text="Save to:").pack(pady=(10, 0))
        location_frame = ttk.Frame(root)
        location_frame.pack()
        # change this next line to set download location
        # but for now we will have it go to the Downloads folder
        self.location_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        ttk.Entry(location_frame, textvariable=self.location_var, width=35).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(location_frame, text="Browse", command=self.browse_location).pack(
            side=tk.LEFT
        )

        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.status = ttk.Label(root, text="Ready", wraplength=450)
        self.status.pack()

        ttk.Button(root, text="Download", command=self.start_download).pack(pady=10)

    def browse_location(self):
        folder = filedialog.askdirectory()
        if folder:
            self.location_var.set(folder)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return

        thread = threading.Thread(target=self.download)
        thread.daemon = True
        thread.start()

    def progress_hook(self, d):
        if d["status"] == "downloading":
            if "total_bytes" in d:
                percent = (d["downloaded_bytes"] / d["total_bytes"]) * 100
            elif "total_bytes_estimate" in d:
                percent = (d["downloaded_bytes"] / d["total_bytes_estimate"]) * 100
            else:
                percent = 0

            self.progress["value"] = percent
            self.status.config(text=f"Downloading...{percent:.0f}%")
            self.root.update_idletasks()

    def download(self):
        # download function
        try:
            self.status.config(text="Starting download...")

            download_type = self.download_type.get()
            save_path = self.location_var.get()

            opts = {
                "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
                "progress_hooks": [self.progress_hook],
                "merge_output_format": "mp4",
            }

            if download_type == "Audio Only":
                opts["format"] = "bestaudio"
                opts["outtmpl"] = os.path.join(save_path, "%(title)s.%(ext)s")
            elif download_type == "Video Only (720p)":
                opts["format"] = "bestvideo[height<=720]"
            else:  # Video (Best) - gets best video without needing merge
                opts["format"] = "best"

            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url_entry.get()])

            self.progress["value"] = 100
            self.status.config(text="Download complete!")
            messagebox.showinfo("Success", f"Downloaded to:\n{save_path}")

        except Exception as e:
            self.status.config(text="Download failed")
            messagebox.showerror("Error", f"Error: {str(e)}")
        finally:
            self.progress["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
