import os 
import glob 
from PIL import Image 
import pikepdf as Pdf
from time import sleep 
from sys import exit
#Banner
print('\n')
print ('██╗███╗   ███╗ ██████╗████████╗ ██████╗ ██████╗ ██████╗ ███████╗\n██║████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝\n██║██╔████╔██║██║  ███╗  ██║   ██║   ██║██████╔╝██║  ██║█████╗  \n██║██║╚██╔╝██║██║   ██║  ██║   ██║   ██║██╔═══╝ ██║  ██║██╔══╝  \n██║██║ ╚═╝ ██║╚██████╔╝  ██║   ╚██████╔╝██║     ██████╔╝██║     \n╚═╝╚═╝     ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═════╝ ╚═╝   By GreyNom (V5)\n') ;print ('In progress... ')

extensions = [".jpg",".png",".jpeg"]										#Most common extensions, not tested others
drawer = "Pdf_Drawer"														#Name of the folder where images to convert are placed 
folder_drawer = str(drawer + "\\")										
outputFile = "output.pdf"		
finalFiles_runtime=[]		

def img_Tpdf():
	pdf = Pdf.new()

	for ext in extensions: 													# 1. Within each extension, it tries it with the glob function which outputs a list
		for file in sorted(glob.glob(folder_drawer + '*' + ext)): 			# Iterating that list and applying the process of creating the pdf of the 												
			name, extension = file.split('.')								# image and merging it to the main one with each 
			final_name = name + '.pdf'
			finalFiles_runtime.append(final_name)											
			with Image.open(file) as image :								#PROCESS 1 : Converting image to PDF			
				im = image.convert('RGB')										
				im.save(final_name)											#PROCESS 2 : Merging all pdfs in one	
			with Pdf.open(final_name) as src:									
				pdf.pages.extend(src.pages)										
				print("██ ",end = "")
				print(file)									
	pdf.save(outputFile)		
	if len(pdf.pages) < 1: 
		print ("NO IMAGE FILES FOUND (JPG,JPEG,PNG)\nAttempting to merge pdfs...") ;os.remove(outputFile); return 1 #Triggers pdf merging try  
	else:						
		print('Files used:',len(finalFiles_runtime))
		for extra_pdfs in finalFiles_runtime : 								#Deleting single pdfs created in PROCESS 1
			os.remove(extra_pdfs)
		return 0

if img_Tpdf() == 1: 														#Merging PDF's if there's no images to convert
	pdf = Pdf.new()
	counter = 0 
	for merging_files in sorted(glob.glob(folder_drawer+'*.pdf')):
		with Pdf.open(merging_files) as src:									
			pdf.pages.extend(src.pages)										
			print("██",end = "")								
			print(merging_files)
			counter += 1 
	pdf.save(outputFile)		
	if len(pdf.pages) < 1: print ("WARNING: NOT ENOUGH ITEMS FOR CREATING PDF"); os.remove(outputFile); exit()
	print('Files used:',counter)

"""
V5 of Image to PDF converter -- By GreyNom at 11/09/2021 # For Python 3 
OLD: 	Solved the error 'PermissionError: [WinError 32] The process cannot access the file because it is being used by another process' by using 
		WITH and AS strucutre, being used to close a file after opening and being more readeable (07/06/2021)
		Reduced the main process to a single for loop 
		Modified to be used as an exe with Pycharm:	- Absolute path deleted, so Pdf_Drawer must be in same directory as the exe
		Added banner to look prettier
NEWER:
	Added the ability to merge pdf's if there's no images to convert in last place
"""