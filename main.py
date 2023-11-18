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
import subprocess
import os
celestial_objects = []  # Global declaration
celestial_stats= []  # Global declaration


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def write_config(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)



def save_config(paths):
    config = read_config()
    config['Directories'] = {'root_paths': ';'.join(paths)}
    write_config(config)




def add_root_directory():
    directory = filedialog.askdirectory()
    if directory:
        config = read_config()  # Read the current config

        # Fetch existing root paths and split into a list, handling the case where the key might not exist
        existing_paths = config.get('Directories', 'root_paths', fallback='').split(';') if config.has_section('Directories') else []

        if directory not in existing_paths:
            existing_paths.append(directory)  # Append the new directory to the list

        # Save the updated paths back to the config
        save_config(existing_paths)






def create_menu(root):
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Select Root Directory", command=add_root_directory)
    #file_menu.add_command(label="Set Sirilic Path", command=set_sirilic_path)


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

def stack_setup():
    print("Stack setup called")  # Debugging line
    if check_and_select_directory():
        print("Directory selected:", root.directory)  # Debugging line
        parse_directories_and_log_stats(root.directory)



def stack_setup():
    global celestial_objects, celestial_stats
    if check_and_select_directory():
        celestial_objects, celestial_stats = parse_directories_and_log_stats(root.directory)
        update_object_list(celestial_objects)

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

def update_object_list(celestial_objects):
    for obj in celestial_objects:()



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


def parse_directories_and_log_stats(root_dir):
    celestial_stats = {}

    for directory in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, directory)
        if os.path.isdir(dir_path):
            json_file_path = os.path.join(dir_path, 'shotsInfo.json')
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as file:
                    data = json.load(file)
                    target = data.get('target', '').strip()
                    exp = data.get('exp', 0)
                    frames_taken = data.get('shotsTaken', 0)
                    total_integration = exp * frames_taken

                    if target not in celestial_stats:
                        celestial_stats[target] = {'total_frames': 0, 'total_integration': 0}
                    celestial_stats[target]['total_frames'] += frames_taken
                    celestial_stats[target]['total_integration'] += total_integration


    print("Parsing directories in", root_dir)  # Debugging line
    # Displaying results and storing them for further interaction
    log_message("Here is a summary of all of the Objects you've captured. Keep up the great work.")
    celestial_objects = list(celestial_stats.keys())
    for index, target in enumerate(celestial_objects, start=1):
        stats = celestial_stats[target]
        message = f"{index}. {target}: Total Frames = {stats['total_frames']}, Total Integration Time = {stats['total_integration']} seconds"
        log_message(message)

    return celestial_objects, celestial_stats
def save_sirilic_path(sirilic_path):
    config = read_config()
    config['Settings'] = {'sirilic_path': sirilic_path}
    write_config(config)




def user_select_object(celestial_objects):
    while True:
        try:
            user_choice = int(input("Enter the number of the object you want to process: "))
            if 1 <= user_choice <= len(celestial_objects):
                return celestial_objects[user_choice - 1]
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")
def log_message(message):
    console_log.configure(state='normal')  # Enable editing of the widget
    if isinstance(message, list):
        for msg in message:
            console_log.insert(tk.END, msg + '\n')  # Display each message on a new line
    else:
        console_log.insert(tk.END, message + '\n')  # For a single message
    console_log.configure(state='disabled')  # Disable editing of the widget
    console_log.see(tk.END)  # Scroll to the bottom
def combine_datasets():
    if not check_and_select_directory():
        log_message("No directory selected. Please select a directory first.")
        return

    root_path = root.directory
    dir_dict = {}

    # Grouping directories by their base names (before the first "_")
    for directory in os.listdir(root_path):
        dir_path = os.path.join(root_path, directory)
        if os.path.isdir(dir_path) and "_" in directory and not directory.endswith("Megadump") and not directory.startswith("Manual_"):
            base_name = directory.split("_")[0]
            if base_name not in dir_dict:
                dir_dict[base_name] = []
            dir_dict[base_name].append(directory)

    # Combining directories and moving files
    for base_name, dirs in dir_dict.items():
        mega_dump_dir = os.path.join(root_path, f"MEGADUMP_{base_name}")
        os.makedirs(mega_dump_dir, exist_ok=True)

        for directory in dirs:
            dir_path = os.path.join(root_path, directory)
            for file in os.listdir(dir_path):
                if file.endswith('.fits'):
                    source_file_path = os.path.join(dir_path, file)
                    unique_filename = f"{directory}_{file}"  # Prepend the source directory name to ensure uniqueness
                    destination_file_path = os.path.join(mega_dump_dir, unique_filename)

                    if not os.path.exists(destination_file_path):
                        shutil.move(source_file_path, destination_file_path)
                        log_message(f"Moved '{file}' from {directory} to '{unique_filename}' in {mega_dump_dir}")
                        # Force GUI to update display
                        root.update_idletasks()
                    else:
                        log_message(f"Skipped '{file}' from {directory} as it already exists in {mega_dump_dir}")
                        # Force GUI to update display
                        root.update_idletasks()

        log_message(f"Combined datasets for {base_name} into {mega_dump_dir}")
        # Force GUI to update display
        root.update_idletasks()



def process_selection():
    global celestial_objects
    try:
        user_choice = int(entry.get())
        if 1 <= user_choice <= len(celestial_objects):
            selected_object = celestial_objects[user_choice - 1]
            log_message(f"User selected {selected_object}")
        else:
            log_message("Invalid choice, please try again.")
    except ValueError:
        log_message("Please enter a valid number.")


root_paths = read_config()
def clean_up_root():
    if not check_and_select_directory():
        log_message("No directory selected. Please select a directory first.")
        return

    root_path = root.directory

    # Create directories if they don't exist
    png_dir = os.path.join(root_path, "PNG")
    jpeg_dir = os.path.join(root_path, "JPEG")
    mp4_dir = os.path.join(root_path, "MP4")

    for directory in [png_dir, jpeg_dir, mp4_dir]:
        os.makedirs(directory, exist_ok=True)

    # Move files to respective folders
    for file in os.listdir(root_path):
        file_path = os.path.join(root_path, file)

        if file.lower().endswith('.jpeg'):
            destination_dir = jpeg_dir
        elif file.lower().endswith('.png'):
            destination_dir = png_dir
        elif file.lower().endswith('.mp4'):
            destination_dir = mp4_dir
        else:
            continue  # Skip files that don't match the extensions

        if os.path.isfile(file_path):
            shutil.move(file_path, os.path.join(destination_dir, file))
            log_message(f"Moved '{file}' to '{destination_dir}'")

    log_message("Cleaned up root directory.")
    # Force GUI to update display
    root.update_idletasks()

# Main window setup
root = tk.Tk()
root.title("Mini Observatory Data Manager")
root.geometry("1280x720")
root.configure(bg="black")

# Menu creation
create_menu(root)

# Frame for left-side buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(side="left", fill="y", padx=5, pady=5)

# Buttons for various operations
buttons = {
    "Rename Directories": rename_directories,
    "Rename All Images": rename_images,
    "Delete all 'Dwarf GOTO' folders": delete_dwarf_goto_dirs,
    "Clean Up Root": clean_up_root,
    "Analyze Datasets": stack_setup,
    "Combine Datasets": combine_datasets,
    #"Run Sirilic": run_sirilic,
}

# Packing the operation buttons
for btn_text, command in buttons.items():
    button = tk.Button(button_frame, text=btn_text, command=command, bg="black", fg="white")
    button.pack(fill="x", padx=5, pady=5)

# Frame for selection and submit
selection_frame = tk.Frame(root, bg="black")
selection_frame.pack(side="top", fill="x", pady=10)

# Entry for user selection
entry = tk.Entry(selection_frame)
entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)



# Frame for console log
console_frame = tk.Frame(root, bg="black")
console_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

# Console log with vertical scrollbar
console_log = tk.Text(console_frame, height=10, state='disabled', bg="black", fg="white", wrap=tk.WORD)
console_scrollbar = tk.Scrollbar(console_frame, command=console_log.yview)
console_log['yscrollcommand'] = console_scrollbar.set
console_scrollbar.pack(side="right", fill="y")
console_log.pack(side="left", fill="both", expand=True)

# Start the main loop
root.mainloop()


