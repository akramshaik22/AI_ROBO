# Classifying Image DataSet

import cv2
import pandas as pd
import numpy as np
import csv
# import time

dat = ['right', 'left', 'front', 'back', 'stop', 'none']
file = open(f"D:/Programming/VS Code/Python/pdc/trainData/train_set_mask.csv", 'w', newline='')
wrtr = csv.writer(file)
for ind, i in enumerate(dat):
    # file = open(f"D:/Programming/VS Code/Python/pdc/trainData/{i}_train_set.csv", 'w', newline='')
    # wrtr = csv.writer(file)
    num = 3001
    if ind == 5:
        num = 3001
    for j in range(num):
        frame = cv2.imread(f"D:/Programming/VS Code/Python/pdc/trainData/{i}/{str(j)}.jpg", cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0,30,60])
        upper_skin = np.array([20,150,255])
        frame = cv2.inRange(frame, lower_skin, upper_skin)
        # cv2.imwrite(r"D:\Programming\VS Code\Python\pdc\trainData\mask_img", frame)
        # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame,(60,60), interpolation=cv2.INTER_AREA)
        # cv2.imwrite(f"D:/Programming/VS Code/Python/pdc/trainData/{ind+1}/{str(j)}.jpg", frame)
        # cv2.imshow('dd',frame)
        # cv2.imwrite(f"D:/Programming/VS Code/Python/pdc/trainData/img{i}.jpg",frame)
        # input()
        # break
        # print(frame.shape)
        frame=frame.flatten()
        # print(len(frame))
        # break
        frame=np.append(frame,[ind])
        frame = list(frame)
        # print(frame)
        # break
        
        wrtr.writerow(frame)
        file.flush()
        # print(frame)
        # break
        # file = pd.concat([file,pd.DataFrame(frame)])
    
    # file.close()
# file.to_csv(f"D:/Programming/VS Code/Python/pdc/trainData/train_set.csv")
# file = pd.DataFrame(file)
# print(file)
file.close()
# time.sleep(5)
cv2.destroyAllWindows()