#!/usr/bin/env python3

import mym3
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

Valid=[]
Train=[]
for i in range(len(study_data["valid"]["Path"])):
	for j in range(study_data["valid"]["Count"][i]):
		Valid.append([study_data["valid"]["Path"][i]+"image"+str(j+1)+".png", study_data["valid"]["Label"][i]])
for i in range(len(study_data["train"]["Path"])):
  for j in range(study_data["train"]["Count"][i]):
    Train.append([study_data["train"]["Path"][i]+"image"+str(j+1)+".pmg", study_data["train"]["Label"][i]])
path=Valid[39][0]
RImg=cv2.imread(path,0)
print(path)
#path=Train[3][0]
#print(path)
m3=mym3.mym3edit(RImg)
median=np.median(m3)
mean=np.mean(m3)
std=np.std(m3)
print(mean, median, std)
diff=abs(int(mean-median))
if mean >median:
  lower=10
else:
  lower=0
#print(len(Train))
#closing=cv2.MORPHOLOGY(RImg,0)
edges=cv2.Canny(m3, lower, min(mean, median))
edges1=cv2.Canny(RImg, lower, min(mean, median))
#pixel=np.asarray(RImg, dtype=np.uint8)


plt.subplot(2,2,1),plt.imshow(RImg,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(m3,cmap = 'gray')
plt.title('M3'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(edges1,cmap = 'gray')
plt.title('Canny on Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(edges,cmap = 'gray')
plt.title('Canny on M3'), plt.xticks([]), plt.yticks([])
plt.show()
