#! /usr/bin/env python3

import numpy as np
from PIL import Image
import math

def mym4edit(img):
  pixel = np.asarray(img, dtype=np.uint8)
  edit=pixel.copy()
  for x in range(1, len(edit)-1):
    for y in range(1, len(pixel[x])-1):
      #file:///usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf,/etc/modprobe.d/nvidia-installer-disable-nouveau.conf
      edit[x][y]=math.sqrt(( pixel[x-1][y-1]**2 + pixel[x-1][y]**2 + pixel[x-1][y+1]**2 + pixel[x][y-1]**2 + 2*(pixel[x][y]**2) + pixel[x][y+1]**2 + pixel[x+1][y-1]**2 + pixel[x+1][y]**2 + pixel[x+1][y+1]**2)/10)
  edit1=edit.copy()
  for x in range(2, len(edit)-2):
    for y in range(2, len(edit[x])-2):
      edit1[x][y]=math.sqrt(( edit[x-1][y-1]**2 + edit[x-1][y]**2 + edit[x-1][y+1]**2 + edit[x][y-1]**2 + 2*(edit[x][y]**2) + edit[x][y+1]**2 + edit[x+1][y-1]**2 + edit[x+1][y]**2 + edit[x+1][y+1]**2)/10)
      
  return (edit1)
