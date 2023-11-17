# Dwarf 2 Data Manager
# [2023] [BD Jones]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import tkinter as tk
from tkinter import filedialog, Menu
import datetime
import configparser
import shutil
from datetime import datetime


def load_config():
    config_file = 'config.ini'
    config = configparser.ConfigParser()

    # Check if the config file exists
    if not os.path.exists(config_file):
        # Create a default config file
        config['Directories'] = {'root_paths': ''}
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        # Read existing config file
        config.read(config_file)

    paths = config.get('Directories', 'root_paths').split(';') if config.has_section('Directories') else []
    return paths




def save_config(paths):
    config = configparser.ConfigParser()
    config['Directories'] = {'root_paths': ';'.join(paths)}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)



def add_root_directory():
    directory = filedialog.askdirectory()
    if directory:
        if directory not in root_paths:
            root_paths.append(directory)  # Use append for list
        save_config(root_paths)


def create_menu(root):
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Select Root Directory", command=add_root_directory)


def check_and_select_directory():
    if 'directory' not in root.__dict__ or not root.directory:
        return select_directory()
    return True


def select_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        root.directory = selected_directory
        save_config([root.directory])
        return True
    return False


def rename_directories():
    if check_and_select_directory():
        root_path = root.directory
        renamed_dirs = []
        for directory in os.listdir(root_path):
            if directory.startswith("DWARF_RAW"):
                dir_path = os.path.join(root_path, directory)
                if os.path.isdir(dir_path):
                    json_file_path = os.path.join(dir_path, 'shotsinfo.json')
                    if os.path.exists(json_file_path):
                        with open(json_file_path, 'r') as file:
                            data = json.load(file)
                            celestial_object = data.get('target', '').strip()

                        if celestial_object:
                            creation_time = os.path.getctime(json_file_path)
                            formatted_time = datetime.fromtimestamp(creation_time).strftime('%Y%m%d_%H%M%S')
                            new_dir_name = f"{celestial_object.replace(' ', '_')}_{formatted_time}"
                            new_dir_path = os.path.join(root_path, new_dir_name)

                            counter = 1
                            original_new_dir_path = new_dir_path
                            while os.path.exists(new_dir_path):
                                new_dir_path = f"{original_new_dir_path}_{counter}"
                                counter += 1

                            os.rename(dir_path, new_dir_path)
                            renamed_dirs.append(f"'{directory}' renamed to '{new_dir_name}'")
        for message in renamed_dirs:
            log_message(message)


def rename_images():
    if check_and_select_directory():
        root_path = root.directory
        for directory in os.listdir(root_path):
            dir_path = os.path.join(root_path, directory)
            if os.path.isdir(dir_path):
                json_file_path = os.path.join(dir_path, 'shotsinfo.json')
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as file:
                        data = json.load(file)
                        celestial_object = data.get('target', '').replace(' ', '_').strip()
                        creation_time = os.path.getctime(json_file_path)
                        date_str = datetime.fromtimestamp(creation_time).strftime('%Y%m%d')

                    for filename in os.listdir(dir_path):
                        if filename.endswith('.fits') and not filename.startswith(celestial_object):
                            old_file_path = os.path.join(dir_path, filename)
                            new_filename = f"{celestial_object}_{date_str}_{filename}"
                            new_file_path = os.path.join(dir_path, new_filename)
                            if os.path.exists(old_file_path):
                                try:
                                    os.rename(old_file_path, new_file_path)
                                    log_message(f"'{filename}' renamed to '{new_filename}'")
                                except OSError as e:
                                    log_message(f"Error renaming file: {e}")


def delete_dwarf_goto_dirs():
    base_path = root.directory
    if not base_path:
        log_message("No directory selected. Please select a directory first.")
        return

    for directory in os.listdir(base_path):
        if directory.startswith("DWARF_GOTO"):
            dir_path = os.path.join(base_path, directory)
            try:
                shutil.rmtree(dir_path)
                log_message(f"Deleted directory: {dir_path}")
            except OSError as error:
                log_message(f"Error deleting directory {dir_path}: {error}")




def log_message(message):
    # Insert the message at the end of the text widget and scroll to the end
    console_log.configure(state='normal')  # Enable editing of the widget
    console_log.insert(tk.END, message + '\n')  # Add newline to separate messages
    console_log.configure(state='disabled')  # Disable editing of the widget
    console_log.see(tk.END)  # Scroll to the bottom



root_paths = load_config()


root = tk.Tk()
root.title("Mini Observatory Data Manager")
root.geometry("800x600")  # Resize for better visibility
root.configure(bg="black")
root.directory = ''

# Create the menu
create_menu(root)

# Frame for buttons on the left
button_frame = tk.Frame(root, bg="black")
button_frame.pack(side="left", fill="y", padx=5, pady=5)  # Changed side to "left"
buttons = {
    "Rename Directories": rename_directories,
    "Rename All Images": rename_images,
}

for btn_text, command in buttons.items():
    button = tk.Button(button_frame, text=btn_text, command=command, bg="black", fg="white")
    button.pack(fill="x", padx=5, pady=5)

delete_button = tk.Button(button_frame, text="Delete all 'Dwarf GOTO' folders", command=delete_dwarf_goto_dirs,
                          bg="black", fg="white")
delete_button.pack(fill="x", padx=5, pady=5)

# Debug console at the bottom
console_frame = tk.Frame(root, bg="black")
console_frame.pack(side="bottom", fill="x", padx=5, pady=5)

# This sets the height of the console_log Text widget to 10 lines (adjust as needed).
console_log = tk.Text(console_frame, height=100, state='disabled', bg="black", fg="white", wrap=tk.WORD)
console_log.pack(side="left", fill="x", expand=True)

# Scrollbar for the console_log
console_scrollbar = tk.Scrollbar(console_frame, command=console_log.yview)
console_scrollbar.pack(side="left", fill="y")
console_log['yscrollcommand'] = console_scrollbar.set  # Link scrollbar to console_log
log_message(
    "Please select a directory first by clicking 'File' and then clicking 'Select Root Directory'. Rename Directories button will rename each sub-directory to whatever the object name is in that directories shots.Info.json. Rename All Images button will append object name and date prior to the frame number for all images in all sub-directories.")
root.mainloop()

