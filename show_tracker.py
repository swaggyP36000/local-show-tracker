import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import json

class ShowTracker:
    def __init__(self, master):
        self.master = master
        master.title("TV Show Tracker")

        # Set the ttk theme to modern
        style = ttk.Style()
        style.theme_use('clam')

        self.show_data = self.load_data()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.master, text="TV Show Tracker", font=("Open Sans", 14))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Show Listbox
        self.listbox = tk.Listbox(self.master, selectmode='single', width=30)
        self.listbox.grid(row=1, column=0, rowspan=5, padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.load_show_details)

        # Refresh button to load shows from data
        self.refresh_button = ttk.Button(self.master, text="Refresh", command=self.refresh_show_list)
        self.refresh_button.grid(row=6, column=0, padx=10, pady=5)

        # Details Frame
        self.details_frame = tk.Frame(self.master, bg="#f7f7f7")
        self.details_frame.grid(row=1, column=1, rowspan=6, padx=10, pady=10)

        # Title
        self.title_label = ttk.Label(self.details_frame, text="Title:", font=("Open Sans", 12))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.details_frame, width=30)
        self.title_entry.grid(row=0, column=1)

        # Description
        self.description_label = ttk.Label(self.details_frame, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="w")
        self.description_text = tk.Text(self.details_frame, height=5, width=28)
        self.description_text.grid(row=1, column=1)

        # Season and Episode
        self.season_label = ttk.Label(self.details_frame, text="Season:")
        self.season_label.grid(row=2, column=0, sticky="w")
        self.season_spinbox = tk.Spinbox(self.details_frame, from_=1, to=99, width=5)
        self.season_spinbox.grid(row=2, column=1, sticky="w")

        self.episode_label = ttk.Label(self.details_frame, text="Episode:")
        self.episode_label.grid(row=3, column=0, sticky="w")
        self.episode_spinbox = tk.Spinbox(self.details_frame, from_=1, to=999, width=5)
        self.episode_spinbox.grid(row=3, column=1, sticky="w")

        # Cover Image
        self.cover_image_label = tk.Label(self.details_frame)
        self.cover_image_label.grid(row=4, column=0, columnspan=2, pady=10)

        image_buttons_frame = tk.Frame(self.details_frame)
        image_buttons_frame.grid(row=5, column=0, columnspan=2)

        self.browse_button = ttk.Button(image_buttons_frame, text="Browse Image", command=self.browse_image)
        self.browse_button.pack(side=tk.LEFT, padx=10)

        self.remove_image_button = ttk.Button(image_buttons_frame, text="Remove Image", command=self.remove_cover_image)
        self.remove_image_button.pack(side=tk.LEFT, padx=10)

        # Save/Update Button
        self.save_button = tk.Button(self.details_frame, text="Save/Update", command=self.save_show_data)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Delete Button
        self.delete_button = ttk.Button(self.master, text="Delete Show", command=self.delete_show)
        self.delete_button.grid(row=7, column=0, pady=5)

        self.refresh_show_list()

    def browse_image(self):
        file_path = subprocess.check_output(['kdialog', '--getopenfilename', '/', 'Image files (*.jpg *.jpeg *.png *.gif)']).decode().strip()
        if file_path:
            try:
                img = Image.open(file_path)
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)

                self.cover_image_label.config(image=photo)
                self.cover_image_label.image = photo
                self.cover_image = file_path  # Store the file path
            except Exception as e:
                print(f"Error loading image: {e}")

    def remove_cover_image(self):
        self.cover_image_label.config(image="")
        self.cover_image_label.image = None
        self.cover_image = None

    def refresh_show_list(self):
        """Clears and reloads shows in the Listbox from self.show_data."""
        self.listbox.delete(0, tk.END)
        for show_title in self.show_data:
            self.listbox.insert(tk.END, show_title)

    def load_show_details(self, event=None):
        """Loads show details into the input fields when a show is selected."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected_show = self.listbox.get(index)
            show_details = self.show_data.get(selected_show, {})

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, selected_show)
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert("1.0", show_details.get("description", ""))
            self.season_spinbox.delete(0, tk.END)
            self.season_spinbox.insert(0, show_details.get("season", 1))
            self.episode_spinbox.delete(0, tk.END)
            self.episode_spinbox.insert(0, show_details.get("episode", 1))

            # Load cover image if available
            cover_image_path = show_details.get("cover_image")
            if cover_image_path:
                try:
                    img = Image.open(cover_image_path)
                    img.thumbnail((200, 200))
                    photo = ImageTk.PhotoImage(img)
                    self.cover_image_label.config(image=photo)
                    self.cover_image_label.image = photo
                    self.cover_image = cover_image_path
                except Exception as e:
                    print(f"Error loading image: {e}")
            else:
                self.cover_image_label.config(image="")
                self.cover_image = None

    def save_show_data(self):
        """Saves the show data to the dictionary and updates the Listbox."""
        title = self.title_entry.get()
        description = self.description_text.get("1.0", tk.END).strip()
        season = int(self.season_spinbox.get())
        episode = int(self.episode_spinbox.get())

        self.show_data[title] = {
            "description": description,
            "season": season,
            "episode": episode,
            "cover_image": self.cover_image  # Store the file path
        }

        self.save_data(self.show_data)
        self.refresh_show_list()  # Refresh the list to reflect changes

    def delete_show(self):
        """Deletes the selected show from the tracker."""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            show_to_delete = self.listbox.get(index)
            del self.show_data[show_to_delete]
            self.listbox.delete(index)
            self.save_data(self.show_data)

    def load_data(self):
        """Loads show data from the JSON file."""
        try:
            with open("show_data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self, data):
        """Saves show data to the JSON file."""
        with open("show_data.json", "w") as f:
            json.dump(data, f, indent=4)

root = tk.Tk()
app = ShowTracker(root)
root.mainloop()
