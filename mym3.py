#! /usr/bin/env python3

import numpy as np
from PIL import Image
import math

def mym3edit(img):
  pixel = np.asarray(img, dtype=np.uint8)
  edit=pixel.copy()
  for x in range(1, len(edit)-1):
    for y in range(1, len(pixel[x])-1):
      #file:///usr/lib/modprobe.d/nvidia-installer-disable-nouveau.conf,/etc/modprobe.d/nvidia-installer-disable-nouveau.conf
      edit[x][y]=math.sqrt(( pixel[x-1][y-1]**2 + pixel[x-1][y]**2 + pixel[x-1][y+1]**2 + pixel[x][y-1]**2 + pixel[x][y]**2 + pixel[x][y+1]**2 + pixel[x+1][y-1]**2 + pixel[x+1][y]**2 + pixel[x+1][y+1]**2)/9)
  return edit
