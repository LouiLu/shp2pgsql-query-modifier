import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import filedialog

print(tk.__file__)

def select_shapefile():
    shape_file = filedialog.askopenfilename(initialdir="./", title="Select Shapefile")
    shape_file_entry.delete(0, tk.END)
    shape_file_entry.insert(0, shape_file)

def run_script():
    shape_file = shape_file_entry.get()
    input_file = 'shp2pgsql_init.sql'
    output_file = output_file_entry.get() or 'output.sql'
    output_folder = output_folder_entry.get() or 'outputs'
    schema = schema_entry.get() or 'transportiq'
    database = database_entry.get() or 'iq-map'
    table = table_entry.get() or 'ADABoundary'
    remove_columns = 'bufferdist'
    # remove_columns = remove_columns_entry.get() or 'bufferdist'
    mapping_columns = 'id:name'
    # mapping_columns = mapping_columns_entry.get() or 'id:name'
    # times = times_entry.get()
    forward_import = flag_var.get()

    # Construct the command with the provided arguments
    command = "python shp2pgsql.py {}".format(shape_file)
    
    if input_file:
        command += " -i {}".format(input_file)
    if output_file:
        command += " -o {}".format(output_file)
    if output_folder:
        command += " -O {}".format(output_folder)
    if schema:
        command += " -s {}".format(schema)
    if database:
        command += " -d {}".format(database)
    if table:
        command += " -t {}".format(table)
    # if remove_columns:
    #     command += " -r {}".format(remove_columns)
    # if mapping_columns:
    #     command += " -m {}".format(mapping_columns)
    # if times:
    #     command += " -T {}".format(times)
    if forward_import:
        command += " -f"

    # Create a subprocess and capture the output
    print('Executing shp2pgsql command: ' + command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    # Convert the output and error to strings
    output = output.decode('utf-8') if output is not None else ""
    error = error.decode('utf-8') if error is not None else ""
    
    # Display the output in the console output area
    console_output.delete(1.0, tk.END)  # Clear the existing content
    console_output.insert(tk.END, output)
    console_output.insert(tk.END, error)

# Create the tkinter window
window = tk.Tk()
window.title("Import shapefile")

# Create a style object
style = ttk.Style()

# Set style properties for specific elements
style.configure("TLabel", foreground="blue", font=("Helvetica", 12, "bold"))
style.configure("TButton", foreground="white", background="blue", font=("Helvetica", 12, "bold"))

# Create section titles
input_section = ttk.Label(window, text="Input Files")
input_section.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))

# Create labels and entry fields for each argument
shape_file_label = ttk.Label(window, text="Shapefile:", anchor='w')
shape_file_label.grid(row=1, column=0, sticky=tk.E, padx=10)
shape_file_entry = ttk.Entry(window)
shape_file_entry.grid(row=1, column=1, padx=10)
browse_button = ttk.Button(window, text="Browse", command=select_shapefile)
browse_button.grid(row=1, column=2, padx=10)

# input_file_label = ttk.Label(window, text="File name:", anchor='w')
# input_file_label.grid(row=2, column=0, sticky=tk.E, padx=10)
# input_file_entry = ttk.Entry(window)
# input_file_entry.grid(row=2, column=1, padx=10)

output_section = ttk.Label(window, text="Output Files", anchor='w')
output_section.grid(row=3, column=0, sticky=tk.W, padx=10, pady=(10, 5))

output_file_label = ttk.Label(window, text="File name:", anchor='w')
output_file_label.grid(row=4, column=0, sticky=tk.E, padx=10)
output_file_entry = ttk.Entry(window)
output_file_entry.grid(row=4, column=1, padx=10)

output_folder_label = ttk.Label(window, text="Folder name:", anchor='w')
output_folder_label.grid(row=5, column=0, sticky=tk.E, padx=10)
output_folder_entry = ttk.Entry(window)
output_folder_entry.grid(row=5, column=1, padx=10)

database_section = ttk.Label(window, text="Database Configuration", anchor='w')
database_section.grid(row=6, column=0, sticky=tk.W, padx=10, pady=(10, 5))

schema_label = ttk.Label(window, text="Schema:", anchor='w')
schema_label.grid(row=7, column=0, sticky=tk.E, padx=10)
schema_entry = ttk.Entry(window)
schema_entry.grid(row=7, column=1, sticky=tk.E, padx=10)

database_label = ttk.Label(window, text="Database:", anchor='w')
database_label.grid(row=8, column=0, sticky=tk.E, padx=10)
database_entry = ttk.Entry(window)
database_entry.grid(row=8, column=1, sticky=tk.E, padx=10)

table_label = ttk.Label(window, text="Table:", anchor='w')
table_label.grid(row=9, column=0, sticky=tk.E, padx=10)
table_entry = ttk.Entry(window)
table_entry.grid(row=9, column=1, sticky=tk.E, padx=10)

host_label = ttk.Label(window, text="Host:", anchor='w')
host_label.grid(row=10, column=0, sticky=tk.E, padx=10)
host_entry = ttk.Entry(window)
host_entry.grid(row=10, column=1, sticky=tk.E, padx=10)

# remove_columns_label = ttk.Label(window, text="Columns to remove:", anchor='w')
# remove_columns_label.grid(row=10, column=0, sticky=tk.E, padx=10)
# remove_columns_entry = ttk.Entry(window)
# remove_columns_entry.grid(row=10, column=1, sticky=tk.E, padx=10)

# mapping_columns_label = ttk.Label(window, text="Mapping columns:", anchor='w')
# mapping_columns_label.grid(row=11, column=0, sticky=tk.E, padx=10)
# mapping_columns_entry = ttk.Entry(window)
# mapping_columns_entry.grid(row=11, column=1, sticky=tk.E, padx=10)

# times_label = ttk.Label(window, text="File related times:", anchor='w')
# times_label.grid(row=12, column=0, sticky=tk.E, padx=10)
# times_entry = ttk.Entry(window)
# times_entry.grid(row=12, column=1, sticky=tk.E, padx=10)

# Create a checkbox
flag_var = tk.BooleanVar()
forward_import_checkbox = ttk.Checkbutton(window, text="Import into table", variable=flag_var)
forward_import_checkbox.grid(row=13, column=0, sticky=tk.E, padx=10)

# Create a button to run the script
run_button = ttk.Button(window, text="Import", command=run_script)
run_button.grid(row=13, column=2, sticky=tk.W, padx=10, pady=(10, 5))

# Create the console output area
console_output = tk.Text(window, height=8, width=60)
console_output.grid(row=15, column=0, columnspan=3, padx=10, pady=(10, 5))

# Start the tkinter event loop
window.mainloop()