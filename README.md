# image-to-pdf

<p align="center">
  <img src="/icons/icon.png" />
</p>

## Purpose 
An easy way of turning your picture files into a only pdf without uploading any sensitive information to web pages
## Usage 
In the same direcotry the executable is, there must be a folder called Pdf_Drawer (already provided) where files must be placed. 

After executing the program the output.pdf will appear in the same place as the exe.  

Some AI images are provided as an example in the folder, including also the pdf. 
### Python
Dependencies:
```shell
pip install -r requirements.txt
```
Execute by clicking on it or in cmd 
## Windows Executables 
Windows executables are provided for convenience, you can make them yourself by using [Pyinstaller](https://pyinstaller.readthedocs.io/en/stable/usage.html):
```shell 
pip install pyinstaller
```
```shell
pyinstaller --onefile ImgToPdf_V4.py
```