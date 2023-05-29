import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

def execute_script():
    # Add your script execution logic here
    script_path = filedialog.askopenfilename(title="Select Script")
    if script_path:
        try:
            subprocess.check_output(["python", script_path])
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", "Script execution failed: "+ e.output)
    else:
        messagebox.showinfo("Info", "No script selected.")

# Create the main window
window = tk.Tk()
window.title("Script Wrapper")

# Add a button to execute the script
execute_button = tk.Button(window, text="Execute Script", command=execute_script)
execute_button.pack(padx=20, pady=20)

# Start the main event loop
window.mainloop()
