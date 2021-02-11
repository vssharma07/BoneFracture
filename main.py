#! /usr/bin/env python3.9

import math
import mym3
import mym4
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
path=Valid[12][0]
print(len(Valid))
print(len(Train))
RImg=cv2.imread(path,0)
print(path)
#path=Train[3][0]
#print(path)
m3=mym3.mym3edit(RImg)
m4=mym4.mym4edit(RImg)
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
sobelx = cv2.Sobel(m3,cv2.CV_64F,1,0,ksize=5)
abs_sobelx = np.absolute(sobelx)
scaled_sobelx = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
sobely = cv2.Sobel(m3,cv2.CV_64F,0,1,ksize=5)
abs_sobely = np.absolute(sobely)
scaled_sobely = np.uint8(255*abs_sobely/np.max(abs_sobely))
#sobel=math.sqrt(scaled_sobelx**2 + scaled_sobely**2)
grad = cv2.addWeighted(scaled_sobelx, 0.5, scaled_sobely, 0.5, 0)
laplacian = cv2.Laplacian(RImg,cv2.CV_64F)
edges=cv2.Canny(RImg, 0, 10)
edges1=cv2.Canny(m4, 0, 10)
#pixel=np.asarray(RImg, dtype=np.uint8)
gray = np.float32(edges1)
dst = cv2.cornerHarris(gray,3,3,0.04)
plt.subplot(2,2,1),plt.imshow(RImg,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(edges,cmap = 'gray')
plt.title('Original Image Canny'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(m4,cmap = 'gray')
plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobel,cmap = 'gray')
plt.title('Filtered Image Canny'), plt.xticks([]), plt.yticks([])
plt.show()
