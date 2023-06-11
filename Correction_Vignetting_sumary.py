print(
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 16:40:05 2023

@author: r.gachlou
Gmail:gachlou.reza@gmail.com
github:gachlou
Program is running.
Please check new folder in directory.
When the processing finished this window will be closed.

** notice: you must run this program in same images path.**
"""
)
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import math 
import glob
import os
import time


temp0=os.path.isdir('new')
if temp0 is False:
   ir_path_new=os.mkdir('new')
tif=glob.glob( '*.tif')


for file in tif:

    im = Image.open(file)
    # extract EXIF data
    exifdata = im.getexif()
    temp1=[]
    temp2=[]

    for tag_id in exifdata:

        # get the tag name, instead of human unreadable tag id
        tag= TAGS.get(tag_id, tag_id)

        temp1.append(tag)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        temp2.append(data)
    
    XMP_dji=temp2[temp1 .index("XMLPacket")]
    list_XMP=XMP_dji.split()

    CenterX = float((list_XMP[128])[8:-9])     # CenterX=783.953979
    CenterY = float((list_XMP[129])[8:-9])     # CenterY=672.917725
    
    K=[]
    for i in range(6):
        K.append(float((list_XMP[i+118])[8:-9]))

    pixelsNew=np.empty((temp2[1], temp2[0]),float)
    
    for x in range(temp2[1]):
        for y in range(temp2[0]):
            r=math.sqrt(((x-CenterY)**2)+((y-CenterX)**2))
            pixelsNew[x,y]=(K[5]*r**6+K[4]*r**5+K[3]*r**4+K[2]*r**3+K[1]*r**2+K[0]*r+1)
  
    ImageNew=np.multiply(im, pixelsNew)

    
    #  change exif data 
    temp=XMP_dji.split('\n') 
    for line in temp:
            if "drone-dji:VignettingData=" in line:
                indexx=temp.index(line)
                temp[indexx]= '   drone-dji:VignettingData="0 ,0 ,0 ,0 ,0 ,0" '
            if "<Camera:VignettingPolynomial>" in line:
                indexx=temp.index(line)
                temp[indexx+2]="     <rdf:li>0</rdf:li>"
                temp[indexx+3]="     <rdf:li>0</rdf:li>"
                temp[indexx+4]="     <rdf:li>0</rdf:li>"
                temp[indexx+5]="     <rdf:li>0</rdf:li>"
                temp[indexx+6]="     <rdf:li>0</rdf:li>"
                temp[indexx+7]="     <rdf:li>0</rdf:li>"
        
    
    temp=bytes( '\n'.join(temp), 'utf-8')

    exifdata.update([(700,temp)])
#  save images
    
##os.chdir(os.path.join())
    imm = Image.fromarray(ImageNew) 
    imm.save('new\\'+file , exif=exifdata)
   
if len(tif)==0:
   time.sleep(30) 
else:
   print ('done')

      
