import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import cv2
import urllib.request
import numpy as np
import subprocess

a = subprocess.run('arp -a', capture_output=True, text=True)
out = a.stdout.split()
url = 'http://'+out[out.index('e8-db-84-94-61-c0')-1]+'/'
print(url)

def send_command(cmd):
    try:
        urllib.request.urlopen(url+cmd, timeout=1)
    except:
        print('timeout err')

dt = ['right', 'left', 'front', 'back', 'stop', 'none']
ln = [0, 0, 0, 0, 0, 0]

mdl = joblib.load(r"D:\Programming\VS Code\Python\pdc\0RFC_Model_HandSigns.joblib")

vid = cv2.VideoCapture(0)
cnt = 0
while True:
    ret, frame = vid.read()
    frame=cv2.flip(frame,2)
    
    # cv2.imshow('Video', frame)
    gr = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.rectangle(frame,(100,50),(300,250),(0, 0, 0),2)
    cv2.imshow('Video', frame)
    gr = gr[50:251,100:301]
    # print(gr.shape)
    # lower_skin = np.array([0,30,60])
    # upper_skin = np.array([20,150,255])
    # gr = cv2.inRange(gr, lower_skin, upper_skin)
    # cv2.imshow('mask', gr)
    gr = cv2.resize(gr, (60,60), interpolation=cv2.INTER_AREA)
    
    # print(gr.shape)
    gr = gr.flatten()
    # print(pd.DataFrame(gr))
    # break
    gr = pd.DataFrame(gr).transpose()
    # print(d['right'])
    # exit(0)
    try:
        ln[mdl.predict(gr)[0]] += 1
    except:
        print(mdl.predict(gr)[0])
    # print(dt[mdl.predict(gr)[0]])
    cnt += 1

    if cnt == 25:
        print(ln)
        print(dt[ln.index(max(ln))])
        send_command(dt[ln.index(max(ln))])
        cnt = 0
        ln = [0, 0, 0, 0, 0, 0]

    if cv2.waitKey(1) & 0XFF==ord('q'):
        break


vid.release()
# pr=a1.predict(x_test)
cv2.destroyAllWindows()