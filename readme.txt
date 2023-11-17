Dwarf 2 Data Manager

Description

Data Manager is a desktop application designed to efficiently organize and manage astronomical data. Ideal for amateur astronomers and small observatory operators, this user-friendly tool simplifies the sorting, renaming, and maintenance of large collections of observational files.
Features

    Select Root Directory: Set a primary location for your astronomical data.
    Rename Directories: Automatically rename directories based on celestial objects.
    Rename All Images: Rename image files for easy identification.
    Delete 'Dwarf GOTO' folders: Clean up and remove unnecessary directories.

Installation

To install the Data Manager, follow these steps:

    Ensure Python is installed on your system.
    Clone this repository or download the source code.
    (Optional) Create a virtual environment for the project.
    Install required dependencies: pip install -r requirements.txt (if applicable).
    If you want to compile to .exe you can use this:
    Step 1.
                pip install pyinstaller
    Step 2.
                pyinstaller --onefile --noconsole --name "Dwarf 2 Data Manager" main.py
    Step 3. Copy the "Dwarf 2 Data Manager.exe" to your favorite astrophotography directory. When you run the .exe a config.ini will be created in the same directory as the .exe.

Usage

Launch the application by running python main.py. Use the GUI to navigate through various functions like selecting root directories, renaming files and directories, and deleting unwanted folders.
Contributing

License

This project is licensed under the MIT License.

Acknowledgments

    Special thanks to Mistral 7B for its contributions.
    Inspired by the needs of the amateur astronomy community.
