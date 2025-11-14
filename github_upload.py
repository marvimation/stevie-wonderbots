#!/usr/bin/env python3
# github_upload.py - Fully patched GitHub Upload GUI
# Features:
# - Drag & drop files
# - Select Files button
# - GUI stays open
# - Shows Git errors in popup
# - Cute GitHub-style icon support

import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("tkinterdnd2 not installed. Run: pip install tkinterdnd2")
    sys.exit(1)


class GitHubUploadGUI:
    def __init__(self, master):
        self.master = master
        master.title("GitHub Upload")
        master.geometry("500x400")
        
        # Main frame
        self.frame = tk.Frame(master, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Label
        self.label = tk.Label(
            self.frame,
            text="Drag & drop files here or click 'Select Files'",
            font=("Helvetica", 12)
        )
        self.label.pack(pady=10)

        # Listbox for files
        self.file_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.file_listbox.pack(pady=10)

        # Enable drag-and-drop
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Buttons
        self.select_btn = tk.Button(self.frame, text="Select Files", command=self.select_files)
        self.select_btn.pack(pady=5)

        self.upload_btn = tk.Button(self.frame, text="Upload to GitHub", command=self.upload_files)
        self.upload_btn.pack(pady=5)

        # Internal file list
        self.files_to_upload = []

    # Drag-and-drop handler
    def drop_files(self, event):
        files = self.master.tk.splitlist(event.data)
        for f in files:
            if f not in self.files_to_upload:
                self.files_to_upload.append(f)
                self.file_listbox.insert(tk.END, f)

    # File selection dialog
    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files to upload")
        if files:
            for f in files:
                if f not in self.files_to_upload:
                    self.files_to_upload.append(f)
                    self.file_listbox.insert(tk.END, f)

    # Git upload
    def upload_files(self):
        try:
            if not self.files_to_upload:
                messagebox.showinfo("No Files", "Please select files first.")
                return

            # Ensure we are in the correct project folder
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            # Git add
            subprocess.run(["git", "add"] + self.files_to_upload, check=True)

            # Commit
            commit_msg = "Upload via GitHub GUI"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)

            # Push
            subprocess.run(["git", "push", "origin", "main"], check=True)

            messagebox.showinfo("Success", "Files successfully uploaded to GitHub!")

            # Clear the list after upload
            self.file_listbox.delete(0, tk.END)
            self.files_to_upload = []

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Git Error", f"Git command failed:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")


# Launch the GUI
if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()  # supports drag-and-drop
        app = GitHubUploadGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("Error launching GitHub Upload GUI:")
        traceback.print_exc()
        input("Press Enter to exit...")

# --- CONFIGURE THESE ---
repo_path = "/home/snap/Desktop/z_Project_Builder/z_SingLoRA_Project"

commit_message = "Auto-upload from SingLoRA GUI"

try:
    # Stage all changes
    subprocess.run(["git", "add", "."], check=True)
    
    # Commit (ignore "nothing to commit" error)
    result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
    if "nothing to commit" in result.stdout.lower() or "nothing to commit" in result.stderr.lower():
        print("No changes to commit.")
    else:
        print(result.stdout)
    
    # Push
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Files successfully uploaded to GitHub!")
except subprocess.CalledProcessError as e:
    print(f"Git command failed: {e}")
