from os import listdir,remove 
import glob 
from PIL import Image 
import pikepdf as Pdf
from datetime import datetime

#Banner
print ('\n██╗███╗   ███╗ ██████╗████████╗ ██████╗ ██████╗ ██████╗ ███████╗\n██║████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝\n██║██╔████╔██║██║  ███╗  ██║   ██║   ██║██████╔╝██║  ██║█████╗  \n██║██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██╔═══╝ ██║  ██║██╔══╝  \n██║██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝██║     ██████╔╝██║     \n╚═╝╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═════╝ ╚═╝   By Gugeldot (V6)\n')

extensions = ['jpg','png','jpeg']										#Most common extensions, not tested others
drawer = "Pdf_Drawer"													#Name of the folder where images to convert are placed
outputFile = "output.pdf"	 
log_enabled = True
log_filename = "imgTpdf.log"
folder_drawer = str(drawer + "\\")										
finalFiles_runtime=[]	

def log_add(message):
	if log_enabled:
		timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
		message = f"[{timestamp}] {message}"

		with open(log_filename, 'a') as file:
			file.write(message + '\n')

def current_extensions (directory):
	#Returns a list o all the extensions present at the directory

	# Raw list of all files
	archivos = listdir(directory)

	# Store their exts and make them a set for no repetition
	exts=[]
	for archivo in archivos:
		exts.append(archivo.split('.')[1])

	exts = list(set(exts))

	log_add(current_extensions.__name__ + ": File formats extracted from " + directory + ": ["+ ' '.join(exts) + "]")

	return exts 

def check_empty(directory):
	#Check if theres any kind of files in the directory at the extensions accepted
	i = 0
	while i < len(extensions) and extensions[i] not in c_exts: 
		i+=1

	log_add(check_empty.__name__ + ": Empty? [" +' '.join(extensions) + "] : "+ str(i == len(extensions)))

	return i == len(extensions)


def mode_selector(directory):
	flag_pdf = 'pdf' in c_exts
	flag_others = not check_empty(directory) #Invert signal 

	if flag_pdf and flag_others: 
		stdout = "NOTICE: BOTH PROPOUSES DETECTED, CONVERTISION PRIORITIZED"
		img_Tpdf()
	else: 
		if flag_others: 
			stdout = "NOTICE: IMG FILES DETECTED, CONVERTED"
			img_Tpdf()
		elif flag_pdf: 
			stdout = "NOTICE: PDF FILES DETECTED, MERGED"
			pdf_merger()
		else: 
			stdout = "ERROR: NO FILES, ABORTED"
	print (stdout)
	log_add(mode_selector.__name__ + ": " + stdout)
		

	
def pdf_merger(): 
	# Selects all pdfs present and merges them in one
	pdf = Pdf.new()
	counter = 0
	files = sorted(glob.glob(folder_drawer+'*.pdf'))
	for file in files:
		with Pdf.open(file) as src:									
			pdf.pages.extend(src.pages)										
			print("██ " + file )								
		counter += 1 
	pdf.save(outputFile)		
	print('Files used:',counter)


def img_Tpdf():
	pdf = Pdf.new()

	for ext in extensions: 													# 1. Within each extension, it tries it with the glob function which outputs a list
		files = sorted(glob.glob(folder_drawer + '*' + ext))
		for file in files: 													# Iterating that list and applying the process of creating the pdf of the 												
			name, extension = file.split('.')								# image and merging it to the main one with each 
			final_name = name + '.pdf'
			finalFiles_runtime.append(final_name)											
			with Image.open(file) as image :								#PROCESS 1 : Converting image to PDF			
				im = image.convert('RGB')										
				im.save(final_name)											
			with Pdf.open(final_name) as src:								#PROCESS 2 : Merging all pdfs in one		
				pdf.pages.extend(src.pages)										
				print("██ ",end = "")
				print(file)		

	pdf.save(outputFile)		
					
	print('Files used:',len(finalFiles_runtime))
	for extra_pdfs in finalFiles_runtime : 								#Deleting single pdfs created in PROCESS 1
		remove(extra_pdfs)

if __name__ == "__main__":
	log_add("SESSION STARTED---------------")
	c_exts = current_extensions(drawer)
	mode_selector(drawer)	
	log_add("SESSION ENDED---------------")



"""
V6 of Image to PDF converter -- By Gugeldot at 11/06/2024 # For Python 3 
OLD: 	Solved the error 'PermissionError: [WinError 32] The process cannot access the file because it is being used by another process' by using 
		WITH and AS strucutre, being used to close a file after opening and being more readeable (07/06/2021)
		Reduced the main process to a single for loop 
		Modified to be used as an exe with Pycharm:	- Absolute path deleted, so Pdf_Drawer must be in same directory as the exe
		Added banner to look prettier
		Added the ability to merge pdf's if there's no images to convert in last place
NEWER:
	Almost complete refactoring for simplicity and readability
	Primitive log system
"""