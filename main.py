#!/usr/bin/env python3

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd
from tqdm import tqdm

data_cat = ['train', 'valid'] # data categories

def get_study_level_data(study_type):

    study_data = {}
    study_label = {'positive': 1, 'negative': 0}
    for phase in data_cat:
        BASE_DIR = 'MURA-v1.1/%s/%s/' % (phase, study_type)
        patients = list(os.walk(BASE_DIR))[0][1] # list of patient folder names
        study_data[phase] = pd.DataFrame(columns=['Path', 'Count', 'Label'])
        i = 0
        #print(patients)
        for patient in tqdm(patients): # for each patient folder
            for study in os.listdir(BASE_DIR + patient): # for each study in that patient folder
                label = study_label[study.split('_')[1]] # get label 0 or 1
                path = BASE_DIR + patient + '/' + study + '/' # path to this study
                study_data[phase].loc[i] = [path, len(os.listdir(path)), label] # add new row
                i+=1
    return study_data


study_data = get_study_level_data(study_type='XR_ELBOW')

img=[]

for i in range(len(study_data["valid"]["Path"])):
	for j in range(study_data["valid"]["Count"][i]):
		img.append([[study_data["valid"]["Path"][i]+"image"+str(j+1)+".png"], study_data["valid"]["Label"][i]])
path=img[25][0][0]
RImg=cv2.imread(path,0)
print(path)
#closing=cv2.MORPHOLOGY(RImg,0)
edges=cv2.Canny(RImg, 10,30)
pixel=np.asarray(RImg, dtype=np.uint8)
#for x in pixel:
#  for y in x:
#    if y<30:
#      pixel[x,y]=0
#    if y>240:
#      pixel[x,y]=0
#print(type(pixel))
#editimg =Image.fromarray(pixel)

plt.subplot(1,2,1),plt.imshow(RImg,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2),plt.imshow(edges,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.show()
