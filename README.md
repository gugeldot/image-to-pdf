# image-to-pdf

<p align="center">
  <img src="/icons/icon.png" />
</p>

## Purpose 
An easy way of turning your picture files into a only pdf without uploading any sensitive information to web pages

## Usage 
In this tool you would be capable of selecting with total freedom the folder in which your image files are, the order in which they'll appear and the name of the output pdf file within a lot more settings.
Once selected the folder where the files are the program will automatically detect valid files and enable merging and conversion capabilities respectively.

Vintage GUI look but simple, efficient and full of feedback.

## New GUI Implemented!
Conversion screen:
<p align="center"><img src="/icons/convert.png" /></p>
Merging screen:
<p align="center"><img src="/icons/merge.PNG" /> </p>
Config screen:
<p align="center"><img src="/icons/config.PNG" /></p>

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