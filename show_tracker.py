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

        # Define color attributes
        self.bg_color = "#2E3440"  # Dark background color
        self.fg_color = "#D8DEE9"  # Light text color
        self.accent_color = "#88C0D0"  # Accent color for highlights

        # Call the setup_modern_ui method
        self.setup_modern_ui()

        self.show_data = self.load_data()

        # Create GUI elements
        self.create_widgets()

    def setup_modern_ui(self):
        # Configure a custom style for a modern look
        style = ttk.Style()
        style.theme_use('clam')

        # Define custom colors
        bg_color = "#2E3440"  # Dark background color
        fg_color = "#D8DEE9"  # Light text color
        accent_color = "#88C0D0"  # Accent color for highlights

        # Configure colors for various widget states
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", background=accent_color, foreground=bg_color)
        style.map("TButton", background=[('active', "#81A1C1")])
        style.configure("TEntry", fieldbackground=bg_color, foreground=fg_color)
        style.configure("TSpinbox", fieldbackground=bg_color, foreground=fg_color)

        # Configure the main window
        self.master.configure(bg=bg_color)
        self.master.option_add("*Font", "Roboto 10")
        self.master.option_add("*Background", bg_color)
        self.master.option_add("*Foreground", fg_color)

        # Add some padding to the main window
        self.master.geometry("800x600")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    def create_widgets(self):
        # Configure button styles
        style = ttk.Style()
        style.configure("Custom.TButton", background=self.accent_color, foreground=self.bg_color, padding=10)  # Add padding for height

        # Remove the TV Show Tracker label
        # self.label = tk.Label(self.master, text="TV Show Tracker", font=("Helvetica", 16))
        # self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure Treeview style
        style = ttk.Style()
        style.configure("Treeview", rowheight=60)  # Set the row height to be higher
        style.configure("Treeview", background=self.bg_color, fieldbackground=self.bg_color, foreground=self.fg_color, borderwidth=0)  # Set background and text color, remove border
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])  # Remove borders

        # Show Treeview with cover images
        self.tree = ttk.Treeview(self.master, columns=("Title",), show="tree", selectmode='browse', style="Treeview")
        self.tree.column("#0", width=100)
        self.tree.column("Title", width=200)
        self.tree.grid(row=1, column=0, rowspan=5, columnspan=3, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.load_show_details)

        # Dictionary to hold PhotoImage references
        self.image_refs = {}

        # Details Frame
        self.details_frame = ttk.Frame(self.master)
        self.details_frame.grid(row=1, column=3, rowspan=6, padx=10, pady=10)

        # Title
        self.title_label = ttk.Label(self.details_frame, text="Title:", font=("Open Sans", 12))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title_entry = ttk.Entry(self.details_frame, width=30)
        self.title_entry.grid(row=0, column=1)

        # Description
        self.description_label = ttk.Label(self.details_frame, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="w")
        self.description_text = tk.Text(self.details_frame, height=5, width=28, bg=self.bg_color, fg=self.fg_color)
        self.description_text.grid(row=1, column=1)

        # Season and Episode
        self.season_label = ttk.Label(self.details_frame, text="Season:")
        self.season_label.grid(row=2, column=0, sticky="w")
        self.season_spinbox = ttk.Spinbox(self.details_frame, from_=1, to=99, width=5)
        self.season_spinbox.grid(row=2, column=1, sticky="w")

        self.episode_label = ttk.Label(self.details_frame, text="Episode:")
        self.episode_label.grid(row=3, column=0, sticky="w")
        self.episode_spinbox = ttk.Spinbox(self.details_frame, from_=1, to=999, width=5)
        self.episode_spinbox.grid(row=3, column=1, sticky="w")

        # Cover Image
        self.cover_image_label = ttk.Label(self.details_frame)
        self.cover_image_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Image Buttons Frame
        image_buttons_frame = tk.Frame(self.details_frame)
        image_buttons_frame.grid(row=5, column=0, columnspan=2)

        self.browse_button = ttk.Button(image_buttons_frame, text="Browse Image", command=self.browse_image, style="Custom.TButton", width=15)
        self.browse_button.pack(side=tk.LEFT, padx=10)

        self.remove_image_button = ttk.Button(image_buttons_frame, text="Remove Image", command=self.remove_cover_image, style="Custom.TButton", width=15)
        self.remove_image_button.pack(side=tk.LEFT, padx=10)

        # Action Buttons Frame
        action_buttons_frame = tk.Frame(self.details_frame)
        action_buttons_frame.grid(row=6, column=0, columnspan=2)

        # Delete button (under Browse Image)
        self.delete_button = ttk.Button(action_buttons_frame, text="Delete", command=self.delete_show, style="Custom.TButton", width=15)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        # Save/Update button (under Remove Image)
        self.save_button = ttk.Button(action_buttons_frame, text="Save/Update", command=self.save_show, style="Custom.TButton", width=15)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=(5, 10))

        # Refresh button (under Delete and Save/Update)
        self.refresh_button = ttk.Button(action_buttons_frame, text="Refresh", command=self.refresh_show_list, style="Custom.TButton", width=15)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=(5, 10))

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
        """Clears and reloads shows in the Treeview from self.show_data."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.image_refs.clear()  # Clear previous image references

        for show_title, details in self.show_data.items():
            cover_image_path = details.get("cover_image", "")
            if cover_image_path:
                try:
                    img = Image.open(cover_image_path)
                    img.thumbnail((50, 50))  # Adjust the size as needed
                    photo = ImageTk.PhotoImage(img)
                    self.image_refs[show_title] = photo  # Store reference to prevent garbage collection
                    self.tree.insert("", "end", text="", image=photo, values=(show_title,))
                except Exception as e:
                    print(f"Error loading image: {e}")
                    self.tree.insert("", "end", text="", values=(show_title,))
            else:
                self.tree.insert("", "end", text="", values=(show_title,))

    def load_show_details(self, event=None):
        """Loads show details into the input fields when a show is selected."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            selected_show = item["values"][0]
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

    def save_show(self):
        """Saves or updates the show details."""
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
        """Deletes the selected show from the Treeview and the underlying data structure."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            selected_show = item["values"][0]

            # Remove from the Treeview
            self.tree.delete(selection[0])

            # Remove from the underlying data structure
            if selected_show in self.show_data:
                del self.show_data[selected_show]

            # Save the updated data to the JSON file
            self.save_data_to_json()

            # Clear the input fields
            self.title_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)
            self.season_spinbox.delete(0, tk.END)
            self.episode_spinbox.delete(0, tk.END)
            self.cover_image_label.config(image="")
            self.cover_image = None

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

    def save_data_to_json(self):
        """Saves the current show data to the JSON file."""
        with open('show_data.json', 'w') as json_file:
            json.dump(self.show_data, json_file, indent=4)

root = tk.Tk()
app = ShowTracker(root)
root.mainloop()
