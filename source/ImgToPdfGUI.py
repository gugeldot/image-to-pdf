from tkinter import *
from tkinter.ttk import Notebook, Separator
from tkinter import filedialog
from PIL import Image, ImageTk
from lib import ImgToPdf_V7 as itp
import json
import os

Image.MAX_IMAGE_PIXELS = None
imgPath = "Imgs/"
# TK initialization
root = Tk()
root.iconbitmap(imgPath+"icon.ico")
root.title("ImgToPDF")
root.resizable(False, False)

# Config autoregen
itp.check_config()

# Vars
config_filename = itp.config_filename
config = itp.config_load(config_filename)
valid_extensions = ('.png', '.jpg', '.jpeg')
files = [f for f in os.listdir(config['drawer']) if f.lower().endswith(valid_extensions)]
pdfs = [f for f in os.listdir(config['drawer']) if f.lower().endswith(('.pdf',))]
bold_font = ("TkDefaultFont", 12, "bold")
drawer_path = StringVar(value=config['drawer'])
output_path = StringVar(value=config['location'])
status_message = StringVar()
status_message_pdf = StringVar()
pdf_path = StringVar()  
open_pdf_button = None
open_pdf_button2 = None
selected_file = None
selected_pdf = None

# Screen stuff
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.2)
window_height = int(screen_height * 0.45)
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Tab system
tab_control = Notebook(root)
tab1 = Frame(tab_control)
tab2 = Frame(tab_control)
tab3 = Frame(tab_control)
tab_control.add(tab1, text="Convert")
tab_control.add(tab2, text="Merge")
tab_control.add(tab3, text="Config")
tab_control.pack(expand=1, fill="both", padx=10, pady=10)


def refreshTab(tab):
    for widget in tab.winfo_children():
        widget.destroy()
    load_config()
    update_tabs_visibility()

def select_drawer():
    path = filedialog.askdirectory()
    if path:
        drawer_path.set(path)
    refreshTab(tab3)

def select_output():
    path = filedialog.askdirectory()
    if path:
        output_path.set(path)
    refreshTab(tab3)

def firstCheckBoxState(new_state):
    checkbox_state.set(new_state)

def separatorTab3(rowA):
    separator = Separator(tab3, orient='horizontal')
    separator.grid(row=rowA, column=0, columnspan=3, sticky='ew', pady=10)
    tab3.grid_columnconfigure(0, weight=1)

def save_changes(drawer_path, ofValue, checkbox_state, logFValue):
    global files
    global pdfs
    save_drawer_path = drawer_path.get()
    save_ofValue = ofValue.get()
    save_oPValue = output_path.get()
    save_checkbox_state = True if checkbox_state.get() == 1 else False
    save_logFValue = logFValue.get()

    config["drawer"] = save_drawer_path
    config["outputFile"] = save_ofValue
    config["location"] = save_oPValue
    config["log_enabled"] = save_checkbox_state
    config["log_filename"] = save_logFValue

    itp.config_save(config_filename, config)
    refreshTab(tab3)
    files = [f for f in os.listdir(config['drawer']) if f.lower().endswith(valid_extensions)]
    pdfs = [f for f in os.listdir(config['drawer']) if f.lower().endswith(('.pdf',))]
    update_file_list()
    update_pdf_list()

def reload_config():
    itp.config_save(config_filename, itp.default_config)
    drawer_path.set(itp.default_config['drawer'])
    output_path.set(itp.default_config['location'])
    refreshTab(tab3)



def truncate_path(path_str, parts_to_show):
    path_parts = path_str.split('/')
    if len(path_parts) > parts_to_show:
        truncated_path = '/'.join(path_parts[:parts_to_show])
        if len(path_parts) > parts_to_show + 1:
            truncated_path += '/...'
        truncated_path += '/' + path_parts[-1]
    else:
        truncated_path = path_str

    return truncated_path

def load_config():
    global drawer_path, output_path  

    with open(config_filename, 'r') as file:
        config = json.load(file)

    Label(tab3, text="General configuration", font=bold_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
    separatorTab3(1)

    Label(tab3, text="Drawer folder:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
    Button(tab3, text="Select Drawer", command=select_drawer).grid(row=2, column=1, padx=5, pady=5)

    parts_to_show_drawer = 5
    drawer_path_label_text = truncate_path(drawer_path.get(), parts_to_show_drawer)
    drawer_path_label = Label(tab3, text=drawer_path_label_text)
    drawer_path_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=W)

    separatorTab3(4)

    Label(tab3, text="Output File:").grid(row=5, column=0, padx=5, pady=5, sticky=W)
    ofValue = Entry(tab3)
    ofValue.insert(0, config['outputFile'])
    ofValue.grid(row=5, column=1, padx=5, pady=5)

    Button(tab3, text="Select location", command=select_output).grid(row=6, column=2, padx=5, pady=5)

    
    parts_to_show_output = 3
    output_path_label_text = truncate_path(output_path.get(), parts_to_show_output)
    output_path_label = Label(tab3, text=output_path_label_text)
    output_path_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=W)

    separatorTab3(7)

    Label(tab3, text="Log Enabled:").grid(row=8, column=0, padx=5, pady=5, sticky=W)

    global checkbox_state
    checkbox_state = IntVar()
    checkbox_state.set(1)

    checkbox = Checkbutton(tab3, text="Toggle", variable=checkbox_state)
    checkbox.grid(row=8, column=1, columnspan=2, sticky='ew', pady=10)

    firstCheckBoxState(config['log_enabled'])

    separatorTab3(9)

    Label(tab3, text="Log Filename:").grid(row=10, column=0, padx=5, pady=5, sticky=W)
    logFValue = Entry(tab3)
    logFValue.insert(0, config['log_filename'])
    logFValue.grid(row=10, column=1, padx=5, pady=5)

    separatorTab3(11)

    button_x = window_width // 2
    button_y = window_height - window_height * 0.2

    save = Button(tab3, text="Save Changes", command=lambda: save_changes(drawer_path, ofValue, checkbox_state, logFValue))
    save.place(x=button_x, y=button_y, anchor="center")

    reload = Button(tab3, text="Reload default config", command=reload_config)
    reload.place(x=button_x + button_x * 0.6, y=button_y, anchor="center")


def update_tabs_visibility(event=None):
    c_exts = itp.current_extensions(drawer_path.get(), config)

    if not itp.check_empty(drawer_path.get(), config):
        tab_control.tab(tab1, state='hidden')
    else:
        tab_control.tab(tab1, state='normal')


    if 'pdf' not in c_exts:
        tab_control.tab(tab2, state='hidden')
    else:
        tab_control.tab(tab2, state='normal')

def scroll_left():
    global files, selected_file
    try:
        indexFile = files.index(selected_file) 
        if indexFile > 0:
            files[indexFile], files[indexFile - 1] = files[indexFile - 1], files[indexFile]
        else:
            files.append(files.pop(indexFile))
        update_file_list() 
    except ValueError:
        print(f"Error: selected_file {selected_file} not found in files list.")

def scroll_left_pdf():
    global pdfs, selected_pdf
    try:
        indexPdf = pdfs.index(selected_pdf)
        if indexPdf > 0:
            pdfs[indexPdf], pdfs[indexPdf - 1] = pdfs[indexPdf - 1], pdfs[indexPdf]
            selected_pdf = pdfs[indexPdf - 1]  
        else:
            pdfs.append(pdfs.pop(indexPdf))

    except ValueError:
        print(f"Error: selected_pdf {selected_pdf} not found in pdfs list.")
    update_pdf_list()

def scroll_right():
    global files, selected_file
    try:
        indexFile = files.index(selected_file) 
        if indexFile < len(files) - 1:
            files[indexFile], files[indexFile + 1] = files[indexFile + 1], files[indexFile]
        else:
            files.insert(0, files.pop(indexFile))
  
        update_file_list()  
    
    except ValueError:
        print(f"Error: selected_file {selected_file} not found in files list.")

def scroll_right_pdf():
    global pdfs, selected_pdf
    try:
        indexPdf = pdfs.index(selected_pdf)
        if indexPdf < len(pdfs) - 1:
            pdfs[indexPdf], pdfs[indexPdf + 1] = pdfs[indexPdf + 1], pdfs[indexPdf]
            selected_pdf = pdfs[indexPdf + 1]  
        else:
            pdfs.insert(0, pdfs.pop(indexPdf))
    except ValueError:
        print(f"Error: selected_pdf {selected_pdf} not found in pdfs list.")
    update_pdf_list()


def update_pdf_list():
    global pdfs, selected_pdf
    for widget in pdf_frame_inner.winfo_children():
        widget.destroy()

    row, col = 0, 0
    for i, file in enumerate(pdfs):
        file_path = os.path.join(drawer_path.get(), file)
        file_name = file

        if len(file_name) > 11:
            Dot = file_name.rfind('.')
            ext = file_name[Dot + 1:]
            old = file_name[:11]
            file_name = f"{old}...{ext}"

        try:
            # Parameters for thumbnails
            thumbnail_size = (80, 80)  # Thumbnail size (width, height)
            thumbnail_padx = 5  # Horizontal padding for thumbnails
            thumbnail_pady = 5  # Vertical padding for thumbnails
            num_columns = 4  # Number of columns for layout

           
            pdf_icon = Image.open(imgPath+"pdf_icon.png")  
            pdf_icon.thumbnail(thumbnail_size)
            pdf_icon = ImageTk.PhotoImage(pdf_icon)
            pdf_label = Label(pdf_frame_inner, image=pdf_icon)
            pdf_label.image = pdf_icon
            pdf_label.grid(row=row, column=col, padx=thumbnail_padx, pady=thumbnail_pady)

            
            name_label = Label(pdf_frame_inner, text=file_name, wraplength=100)
            name_label.grid(row=row + 1, column=col, padx=thumbnail_padx, pady=thumbnail_pady)

            
            pdf_label.bind("<Button-1>", lambda e, file_name=file: handle_pdf_click(file_name))
            name_label.bind("<Button-1>", lambda e, file_name=file: handle_pdf_click(file_name))

           
            if file == selected_pdf:
                pdf_label.config(bg="lightblue")
                name_label.config(bg="lightblue")

            col += 1
            if col == num_columns:  
                col = 0
                row += 2  
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
            continue

def update_file_list():
    global files
    selected_file = None
    config = itp.config_load(config_filename)
    drawer = config['drawer']
  
    # Clear current canvas
    for widget in file_frame_inner.winfo_children():
        widget.destroy()

    valid_extensions = ('.png', '.jpg', '.jpeg')

    row, col = 0, 0
    
    # Parameters for thumbnails
    thumbnail_size = (80, 80)  # Thumbnail size (width, height)
    thumbnail_padx = 5  # Horizontal padding for thumbnails
    thumbnail_pady = 5  # Vertical padding for thumbnails
    num_columns = 4  # Number of columns for layout

    for i, file in enumerate(files):
        file_path = os.path.join(drawer, file)
        name_label_text = file  # Original file name

        MAX_len = 11
        old,ext = name_label_text.split('.')

        if len(old) > MAX_len:
            name_label_text = f"{old[:MAX_len]}...{ext}"

        try:
            # Open the image to check size
            IMG_MAX = 178956970   # Example: Max allowed dimensions
            with Image.open(file_path) as img:
                # Check if image size exceeds the limit
                if img.size[0] * img.size[1] > IMG_MAX:
                    raise ValueError(f"Image size ({img.size}) exceeds maximum allowed dimensions ({IMG_MAX}, {IMG_MAX}) -> No preview icon")
                    itp.log_add(f"update_file_list: Image size ({img.size}) exceeds maximum allowed dimensions ({IMG_MAX}, {IMG_MAX}) -> No preview icon")

                img.thumbnail(thumbnail_size)  # Resize thumbnail
                img = ImageTk.PhotoImage(img)
                label = Label(file_frame_inner, image=img, text=name_label_text, compound=TOP)
                label.image = img
                label.grid(row=row, column=col, padx=thumbnail_padx, pady=thumbnail_pady)  # Adjust padding as needed

            
                label.bind("<Button-1>", lambda e, file_name=file: handle_image_click(file_name))

        except Exception as e:
            # Handle error loading image
            print(f"Error loading image {file_path}: {e}")
            # Show no_preview.png in case of error
            img = Image.open(imgPath+"no_preview.png")
            img.thumbnail(thumbnail_size)  # Resize thumbnail
            img = ImageTk.PhotoImage(img)
            img_label = Label(file_frame_inner, image=img)
            img_label.image = img
            img_label.grid(row=row, column=col, padx=thumbnail_padx, pady=thumbnail_pady)  # Adjust padding as needed

            # Show error file name
            name_label = Label(file_frame_inner, text=name_label_text, wraplength=100)
            name_label.grid(row=row + 1, column=col, padx=thumbnail_padx, pady=thumbnail_pady)  # Adjust padding as needed

        col += 1
        if col == num_columns:
            col = 0
            row += 1

def handle_image_click(file_name):
    global selected_file
    selected_file = file_name
    
def handle_pdf_click(file_name):
    global selected_pdf
    selected_pdf = file_name
    update_pdf_list()


# Función para manejar el clic en el botón "Convertir PDF" en tab2
def handle_pdf_convert_click():
    global open_pdf_button2
    success, pdf_path_value = itp.merge_pdfs(pdfs,config)
    if success:
        status_message_pdf.set(f"All Done!\n Path: {pdf_path_value}")
        status_label.config(fg="green")  # Color verde para indicar éxito
        pdf_path.set(pdf_path_value)  # Actualizar la variable global de la ruta del PDF

        # Crear o actualizar el botón "Abrir PDF"
        if open_pdf_button2 and open_pdf_button2.winfo_exists():
            open_pdf_button2.config(command=lambda: os.startfile(pdf_path.get()))
        else:
            open_pdf_button2 = Button(tab2, text="Open PDF", command=lambda: os.startfile(pdf_path.get()))
            open_pdf_button2.pack(pady=5)

        delete_buttonPdf = Button(tab2, text="Delete pdfs?", command=lambda: handle_delete_pdf(config))
        delete_buttonPdf.pack(pady=5)

    else: 
        status_message_pdf.set("Error en la conversión!")
        status_label_pdf.config(fg="red")  # Color rojo para indicar error

def handle_convert_click():
    global open_pdf_button

    success, pdf_path_value = itp.convert_png(files, config)
    if success:
        status_message.set(f"All Done!\n Path:  {pdf_path_value}")
        status_label.config(fg="green")
        pdf_path.set(pdf_path_value)

        if open_pdf_button and open_pdf_button.winfo_exists():
            open_pdf_button.config(command=lambda: os.startfile(pdf_path.get()))
        else:
            #print(pdf_path.get())
            open_pdf_button = Button(tab1, text="Open PDF", command=lambda: os.startfile(pdf_path.get()))
            open_pdf_button.pack(pady=5)
        
        
        delete_button = Button(tab1, text="Delete files?", command=lambda: handle_delete_files(config))
        delete_button.pack(pady=5)
    else:
        status_message.set("Something went wrong!")
        status_label.config(fg="red")




def handle_delete_files(config):
    itp.cleanDir(config)
    #update_file_list()
    update_tabs_visibility()

def handle_delete_pdf(config):
    print("A")
    itp.cleanDirPDF(config)
    #update_file_list()
    update_tabs_visibility()


#EXECUTION 

load_config()

# TAB1 -------------------------------
Label(tab1, text="Image Files", font=bold_font).pack(padx=10, pady=(10, 5), anchor="w")
frame_height = int(window_height * 0.3)
file_frame = Frame(tab1, height=frame_height, borderwidth=2, relief="solid", bg="black")
file_frame.pack(fill="x", padx=10, pady=10)

button_frame = Frame(tab1)
button_frame.pack(fill="x", padx=10, pady=10)

left_button = Button(button_frame, text="←", command=scroll_left)
left_button.pack(side=LEFT, fill="x", expand=True)

right_button = Button(button_frame, text="→", command=scroll_right)
right_button.pack(side=RIGHT, fill="x", expand=True)

file_canvas = Canvas(file_frame, bg="white")
file_scrollbar = Scrollbar(file_frame, orient=VERTICAL, command=file_canvas.yview)
file_canvas.configure(yscrollcommand=file_scrollbar.set)

file_frame_inner = Frame(file_canvas, bg="white")
file_canvas.create_window((0, 0), window=file_frame_inner, anchor="nw")

file_canvas.pack(side=LEFT, fill="both", expand=True)
file_scrollbar.pack(side=RIGHT, fill="y")

file_frame_inner.bind("<Configure>", lambda e: file_canvas.configure(scrollregion=file_canvas.bbox("all")))

status_label = Label(tab1, textvariable=status_message, fg="green", font=("Arial", 12, "bold"))
status_label.pack(pady=10)

convert_button = Button(tab1, text="Convert", command=handle_convert_click)
convert_button.pack(side="bottom", fill="x", padx=10, pady=10)


# TAB2 -------------------------------
pdf_frame = Frame(tab2, height=frame_height, borderwidth=2, relief="solid", bg="black")
pdf_frame.pack(fill="x", padx=10, pady=10)

button_frame = Frame(tab2)
button_frame.pack(fill="x", padx=10, pady=10)

left_button = Button(button_frame, text="←", command=scroll_left_pdf)
left_button.pack(side=LEFT, fill="x", expand=True)

right_button = Button(button_frame, text="→", command=scroll_right_pdf)
right_button.pack(side=RIGHT, fill="x", expand=True)

pdf_canvas = Canvas(pdf_frame, bg="white")
pdf_scrollbar = Scrollbar(pdf_frame, orient=VERTICAL, command=pdf_canvas.yview)
pdf_canvas.configure(yscrollcommand=pdf_scrollbar.set)

pdf_frame_inner = Frame(pdf_canvas, bg="white")
pdf_canvas.create_window((0, 0), window=pdf_frame_inner, anchor="nw")

pdf_canvas.pack(side=LEFT, fill="both", expand=True)
pdf_scrollbar.pack(side=RIGHT, fill="y")

pdf_frame_inner.bind("<Configure>", lambda e: pdf_canvas.configure(scrollregion=pdf_canvas.bbox("all")))

status_label_pdf = Label(tab2, textvariable=status_message_pdf, fg="green", font=("Arial", 12, "bold"))
status_label_pdf.pack(pady=10)

convert_button = Button(tab2, text="Merge", command=handle_pdf_convert_click)
convert_button.pack(side="bottom", fill="x", padx=10, pady=10)


update_file_list()
update_pdf_list()

update_tabs_visibility()


tab_control.bind("<<NotebookTabChanged>>", update_tabs_visibility)


root.mainloop()

