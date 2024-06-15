from os import listdir,remove,path,getenv
import glob 
from PIL import Image 
import pikepdf as Pdf
from datetime import datetime
import json

Image.MAX_IMAGE_PIXELS = None
desktop_path = path.join(getenv('USERPROFILE'), 'Desktop')
extensions = ['jpg','png','jpeg']	
config_filename = "config.json" 									#Most common extensions, not tested others									
default_config = {"drawer": desktop_path, "outputFile": "output.pdf", "location": "","log_enabled": True, "log_filename": "imgTpdf.log"}


def log_add(message,config):
	if config['log_enabled']:
		timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
		message = f"[{timestamp}] {message}"

		with open(config['log_filename'], 'a') as file:
			file.write(message + '\n')

def config_load(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    log_add(load_config.__name__ + ": Configuration loaded from " + file_path)

def config_save(file_path, config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

    log_add(config_save.__name__ + ": Configuration saved",config)

def check_config():
	if not path.exists(config_filename): 
		config_save(config_filename,default_config)
		log_add(check_config.__name__ + ": Configuration error, default regeneration",default_config)
	else: 
		log_add(check_config.__name__ + ": Configuration okay",default_config)

def current_extensions (directory,config):
	#Returns a list o all the extensions present at the directory

	# Raw list of all files
	archivos = listdir(directory)

	# Store their exts and make them a set for no repetition
	exts=[]

	for archivo in archivos:
		exts.append(archivo.split('.')[-1] if len(archivo.split('.')) > 1 else "None")
	
	
	exts = list(set(exts))
	
	log_add(current_extensions.__name__ + ": File formats extracted from " + directory + ": ["+ ' '.join(exts) + "]",config)

	return exts 


def check_empty(directory,config):
	#Check if theres any kind of files in the directory at the extensions accepted
	c_exts = current_extensions(directory,config)

	for extension in extensions:
		if extension in c_exts:
			log_add(check_empty.__name__ + ": Empty? [" +' '.join(extensions) + "] : False [" + extension + "]",config)
			return True

	log_add(check_empty.__name__ + ": Empty? [" +' '.join(extensions) + "] : True",config)
	
	return False



def merge_pdfs(pdfs,config): 
	drawer = config['drawer'] 
	if len(config['location']) == 0: output = config['outputFile']
	else: output = config['location'] +"/"+ config['outputFile']
	config = config_load (config_filename)
	c_exts = current_extensions(drawer,config)
	flag_pdf = 'pdf' in c_exts
	boole = False

	if flag_pdf:
		pdfs_with_drawer = [drawer + '/'+ f for f in pdfs]
		pdf_merger(pdfs_with_drawer,config)
		log_add(merge_pdfs.__name__ + ": Pdfs merged" ,config)
		if path.exists(output):
			boole = True
	else: 
		log_add(merge_pdfs.__name__ + ": Error, no pdfs?" ,config)
	return boole,output




def pdf_merger(pdfs,config): 
	# Selects all pdfs present and merges them in one
	pdf = Pdf.new()
	counter = 0
	drawer = config['drawer'] 
	for file in pdfs:
		with Pdf.open(file) as src:									
			pdf.pages.extend(src.pages)										
			log_add("[+] " + file,config)								
		counter += 1 

	if len(config['location']) == 0: output = config['outputFile']
	else: output = config['location'] +"/"+ config['outputFile']

	pdf.save(output)		
	log_add('Files used: ' +str(counter),config)	


def convert_png(files,config):
	drawer = config['drawer'] 

	if len(config['location']) == 0: output = config['outputFile']
	else: output = config['location'] +"/"+ config['outputFile']

	config = config_load (config_filename)
	c_exts = current_extensions(drawer,config)
	flag_others = check_empty(drawer,config) #Invert signal 
	boole = False
	if flag_others: 
		files_with_drawer = [drawer + '/'+ f for f in files]
		img_Tpdf(files_with_drawer,config)
		log_add(convert_png.__name__ + ": Pngs converted" ,config)

		
		if path.exists(output):
			boole = True
	else: 
		log_add(convert_png.__name__ + ": Error, no pngs?" ,config)
	return boole,output


from pathlib import Path
import pikepdf as Pdf

def img_Tpdf(files, config):
    extensions = ['jpg', 'png', 'jpeg']
    final_files = []  

    for ext in extensions:
        for file in files:
            if file.lower().endswith(ext):
                name = Path(file).stem
                final_name = f"{name}.pdf"
                with Image.open(file) as image:
                    pdf_path = Path(config['outputFile'])    
                    image.convert('RGB').save(pdf_path.parent / final_name, "PDF")

                final_files.append(str(pdf_path.parent / final_name))
                log_add(f"[+] {file}",config)


    
    if final_files:
        pdf_merger = Pdf.Pdf.new()
        for pdf_file in final_files:
            pdf_merger.pages.extend(Pdf.open(pdf_file).pages)

        output = config['outputFile'] if not config['location'] else f"{config['location']}/{config['outputFile']}"
        pdf_merger.save(output)
        
        
    for pdf_file in final_files:
        Path(pdf_file).unlink(missing_ok=True)
        



"""
V7 of Image to PDF converter -- By Gugeldot at 11/06/2024 # For Python 3 
OLD: 	Solved the error 'PermissionError: [WinError 32] The process cannot access the file because it is being used by another process' by using 
		WITH and AS strucutre, being used to close a file after opening and being more readeable (07/06/2021)
		Reduced the main process to a single for loop 
		Modified to be used as an exe with Pycharm:	- Absolute path deleted, so Pdf_Drawer must be in same directory as the exe
		Added banner to look prettier
		Added the ability to merge pdf's if there's no images to convert in last place
		Almost complete refactoring for simplicity and readability
		Primitive log system
		
NEWER:
	Settings outscaled to json 
	Config regen
	GUI 
"""