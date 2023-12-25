import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, Label
import os
import xml.etree.ElementTree as ET
import time
from PIL import Image, ImageTk  # Importing the PIL library


# Default resolution values
RES_WIDTH = 640
RES_HEIGHT = 640

# Default XML path
XML_path = ""

selected_folder = ""

def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()


def generate_xml():
    footage_folder = filedialog.askdirectory()
    if footage_folder:
        base_directory = os.path.abspath(footage_folder)  # Get the absolute base directory

        filenames = [f for f in os.listdir(footage_folder) if os.path.isfile(os.path.join(footage_folder, f))]
        
        for index, filename in enumerate(filenames):
            if "VALUES_order_numb" in filename:

                values = filename.split("_")
                min_x = float(values[6])
                max_x = float(values[12])
                min_y = float(values[9])
                max_y = float(values[15])

                distance = float(values[17])

                frame_current = str(round(float(values[3])))

                root = ET.Element("annotation")

                xml_declaration = '<?xml version="1.0" encoding="utf-8"?>'
                xml_declaration_element = ET.Comment(xml_declaration)
                root.append(xml_declaration_element)

                ET.SubElement(root, "filename").text = filename
                ET.SubElement(root, "source_footage").text = XML_path + "/" + filename
                ET.SubElement(root, "frame_number").text = frame_current
                ET.SubElement(root, "crop_name").text = XML_path + "/" + filename

                source = ET.SubElement(root, "source")

                ET.SubElement(source, "database").text = ""


                size = ET.SubElement(root, "size")

                ET.SubElement(size, "width").text = str(RES_WIDTH)
                ET.SubElement(size, "height").text = str(RES_HEIGHT)
                ET.SubElement(size, "depth").text = "3"
                ET.SubElement(size, "x_min").text = ""
                ET.SubElement(size, "y_min").text = ""

                ET.SubElement(root, "segmented").text = "Unspecified"
                ET.SubElement(root, "scene").text = ""
                ET.SubElement(root, "is_4k").text = "0"


                object = ET.SubElement(root, "object")

                
                # Create the "Select Name" selection
                object_name = object_names_var.get()
                ET.SubElement(object, "name").text = object_name 



                ET.SubElement(object, "frame").text = frame_current

                bndbox  = ET.SubElement(object, "bndbox")

                ET.SubElement(bndbox, "xmin").text = str(round(min_x * RES_WIDTH))
                ET.SubElement(bndbox, "ymin").text = str(RES_HEIGHT - round(max_y * RES_HEIGHT))
                ET.SubElement(bndbox, "xmax").text = str(round(max_x * RES_WIDTH))
                ET.SubElement(bndbox, "ymax").text = str(RES_HEIGHT - round(min_y * RES_HEIGHT))

                
                ET.SubElement(object, "id").text = frame_current



                # Create the "Select Type" selection
                signal_type = signal_type_var.get()
                ET.SubElement(object, "Type").text = signal_type        


                ET.SubElement(object, "Occluded").text = "0"
                ET.SubElement(object, "difficult").text = "0"
                ET.SubElement(object, "Size").text = "Unspecified"
                ET.SubElement(object, "Position").text = "Unspecified"
                ET.SubElement(object, "On_rails").text = "No"
                ET.SubElement(object, "Pose").text = "Unspecified"
                ET.SubElement(object, "truncated").text = "1"
                ET.SubElement(object, "Distance_from_camera").text = str(round(distance)).replace("-", "")

                tree = ET.ElementTree(root)
                xml_filename = os.path.splitext(filename)[0] + ".xml"
                xml_save_path = os.path.join(footage_folder, xml_filename)  # Updated this line

                tree.write(xml_save_path)
                result_label.config(text=f"XML file '{xml_filename}' saved successfully!")


def update_resolution():
    global RES_WIDTH, RES_HEIGHT
    try:
        RES_WIDTH = int(res_width_entry.get())
        RES_HEIGHT = int(res_height_entry.get())
        resolution_label.config(text=f"Resolution set to {RES_WIDTH} x {RES_HEIGHT}")
    except ValueError:
        resolution_label.config(text="Invalid resolution values!")




def update_xml_path():
    global XML_path
    try:
        XML_path = str(XML_label_entry.get())

        resolution_label.config(text=f"Resolution set to {RES_WIDTH} x {RES_HEIGHT}")
    except ValueError:
        resolution_label.config(text="Invalid resolution values!")




def process():
    global selected_folder
    
    if not selected_folder:
        result_label.config(text="Please select a folder first.")
        return

    filenames = [f for f in os.listdir(selected_folder) if os.path.isfile(os.path.join(selected_folder, f))]
    total_files = len(filenames)
    
    if total_files == 0:
        result_label.config(text="No files found in the selected folder.")
        return
    
    processed_files = 0

    for filename in filenames:
        if "VALUES_order_numb" in filename:
            # Your existing code here
            
            # Update the progress bar
            processed_files += 1
            progress = int((processed_files / total_files) * 100)
            progress_bar['value'] = progress
            window.update_idletasks()
            
            # Display the loader image
            # Add a slight delay to simulate processing
            time.sleep(0.1)
            
            # Hide the loader and reset the progress bar
            progress_bar['value'] = 0
        
    result_label.config(text=f"XML files generated and saved successfully!")
    

# Create the main window
window = tk.Tk()
window.title("XML Generator")

# Set the dimensions of the window (width x height)
window_width = 590
window_height = 1100
window.geometry(f"{window_width}x{window_height}")


script_dir = os.path.dirname(os.path.abspath(__file__))

image_path = os.path.join(script_dir, "Untitled.png")

# Load and display an image in the UI
image = Image.open(image_path)
image = image.resize((400, 400), Image.ANTIALIAS)  # Resize the image
photo = ImageTk.PhotoImage(image)
image_label = Label(window, image=photo)
image_label.pack()


# Create a Progress Bar
progress_bar = ttk.Progressbar(window, length=350, mode='determinate')
progress_bar.pack()


# Create resolution input fields and update button
res_width_label = tk.Label(window, text="Width:")
res_width_label.pack()
res_width_entry = tk.Entry(window)
res_width_entry.pack()

res_height_label = tk.Label(window, text="Height:")
res_height_label.pack()
res_height_entry = tk.Entry(window)
res_height_entry.pack()

update_resolution_button = tk.Button(window, text="Update Resolution", command=update_resolution)
update_resolution_button.pack()

resolution_label = tk.Label(window, text=f"Resolution set to {RES_WIDTH} x {RES_HEIGHT}")
resolution_label.pack()

#////////////////////////////////////////////////////////////////////////////////////

XML_label = tk.Label(window, text="XML path:")
XML_label.pack()
XML_label_entry = tk.Entry(window)
XML_label_entry.pack()

update_xml_path_button = tk.Button(window, text="Update XML path", command=update_xml_path)
update_xml_path_button.pack()


xml_path_label = tk.Label(window, text=f"XML path set to {XML_path}")
xml_path_label.pack()


# Create the "Select Name" selection
signal_type_label = tk.Label(window, text="Select Name:")
signal_type_label.pack()

object_names = ["Signal", "End Of Catenary Hanging Square", "End Of Catenary Vertical Hanging", "No Entry Ground Round", "False Positive", "Animal", "Braking_Shoe"]
object_names_var = tk.StringVar()
object_names_var.set(object_names[0])  # Default selection


object_name_dropdown = ttk.Combobox(window, textvariable=object_names_var, values=object_names,width=50)
object_name_dropdown.pack()


# Create the "Type" selection
signal_type_label = tk.Label(window, text="Select Type:")
signal_type_label.pack()

signal_types = ["Dwarf CAUTION", "Dwarf STOP", "Dwarf GO", "Hanging", "Ground", "False Positive", "Boar", "Unspecified"]
signal_type_var = tk.StringVar()
signal_type_var.set(signal_types[0])  # Default selection


signal_type_dropdown = ttk.Combobox(window, textvariable=signal_type_var, values=signal_types,width=50)
signal_type_dropdown.pack()




# Create the Select Folder button
select_folder_button = tk.Button(window, text="Select Imeges Folder", command=select_folder)
select_folder_button.pack()

# Create the Process button
process_button = tk.Button(window, text="Process to XML Files", command=generate_xml)
process_button.pack()

# Create the label to display the result
result_label = tk.Label(window, text="")
result_label.pack()

# Start the Tkinter event loop
window.mainloop()
