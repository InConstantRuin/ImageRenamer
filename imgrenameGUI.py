import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer")
        self.root.configure(background="#343434")

        self.folder_path = tk.StringVar()
        self.current_index = 0
        self.image_files = []

        self.setup_gui()


    def setup_gui(self):
        # Create a frame for folder selection
        folder_select_frame = tk.Frame(self.root)
        folder_select_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        folder_select_frame.configure(background="#343434")

        self.folder_path_entry = tk.Entry(folder_select_frame,
                                          textvariable=self.folder_path,
                                          width=50)
        self.folder_path_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.folder_path_entry.configure(background="#565656", foreground="#F3F3F3")
        folder_select_button = tk.Button(folder_select_frame,
                                         text="SELECT FOLDER",
                                         command=self.select_folder)
        folder_select_button.grid(row=0, column=1)
        folder_select_button.configure(background="#565656", foreground="#F3F3F3")

        # Create a frame for image display
        self.image_frame = tk.Frame(self.root)
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.image_frame.configure(background="#565656")
        self.root.grid_rowconfigure(1, weight=1)  # Make the frame resizeable vertically
        self.root.grid_columnconfigure(0, weight=1)  # Make the frame resizeable horizontally

        # Create a label for displaying the image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(fill="both", expand=True)
        self.image_label.configure(background="#565656", foreground="#F3F3F3")

        # Create navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        nav_frame.configure(background="#343434")
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=2)
        nav_frame.grid_columnconfigure(2, weight=1)

        self.prev_button = tk.Button(nav_frame,
                                     text="<< PREV",
                                     command=self.show_prev_image)
        self.prev_button.grid(row=0, column=0, sticky="w")
        self.prev_button.grid_columnconfigure(0, weight=1)
        self.prev_button.configure(background="#565656", foreground="#F3F3F3")

        self.filename_label = tk.Label(nav_frame,
                                       text="",
                                       font=("Arial", 18),
                                       background="#343434",
                                       foreground="#F3F3F3")
        self.filename_label.grid(row=0, column=1, sticky="ew")
        self.filename_label.config(anchor="center")

        self.next_button = tk.Button(nav_frame,
                                     text="NEXT >>",
                                     command=self.show_next_image)
        self.next_button.grid(row=0, column=2, sticky="e")
        self.next_button.configure(background="#565656", foreground="#F3F3F3")

        # Create a frame for renaming the image
        self.rename_frame = tk.Frame(self.root, background="#343434")
        self.rename_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.rename_frame.configure(background="#343434")

        self.current_filename = tk.StringVar()
        self.filename_entry = tk.Entry(self.rename_frame,
                                       textvariable=self.current_filename,
                                       width=50)
        self.filename_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.filename_entry.configure(background="#565656", foreground="#F3F3F3")


        # Create save buttons
        save_button = tk.Button(self.rename_frame,
                                text="SAVE",
                                command=self.save_image)
        save_button.pack(side=tk.LEFT)
        save_button.configure(background="#565656", foreground="#F3F3F3")

        self.filename_entry.bind("<Return>", lambda event: self.save_and_next_image())


    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.load_images_from_folder()


    def load_images_from_folder(self):
        folder_path = self.folder_path.get()
        if folder_path and os.path.isdir(folder_path):
            self.image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            self.current_index = 0
            self.show_current_image()
        else:
            self.image_files = []
            self.current_index = 0


    def show_current_image(self):
        if self.image_files:
            image_path = os.path.join(self.folder_path.get(), self.image_files[self.current_index])
            image = Image.open(image_path)
            image.thumbnail((500, 500))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.current_filename.set(self.image_files[self.current_index])

            # Update filename display label
            filename = os.path.splitext(self.image_files[self.current_index])[0]
            self.filename_label.config(text=filename)


    def show_next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
        else:
            self.current_index = 0 # Loop back to start
        self.show_current_image()


    def show_prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.image_files) - 1 # Loop to the end
        self.show_current_image()


    def save_image(self):
        new_filename = self.current_filename.get()
        old_path = os.path.join(self.folder_path.get(), self.image_files[self.current_index])
        new_path = os.path.join(self.folder_path.get(), new_filename)
        os.rename(old_path, new_path)
        self.image_files[self.current_index] = new_filename


    def save_and_next_image(self):
        self.save_image()
        self.show_next_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenamerApp(root)
    root.mainloop()