import cv2
import numpy as np
# from math import atan2, pi
import subprocess
import urllib.request

try:
    a = subprocess.run('arp -a', capture_output=True, text=True)
    out = a.stdout.split()
    url = 'http://'+out[out.index('e8-db-84-94-61-c0')-1]+'/'
    print("~~ Device Connected ~~")
    print("URL : ", url)
except:
    print("!! Cant't Connect to the Device !!")

def send_command(cmd):
    try:
        urllib.request.urlopen(url+cmd, timeout=1)
    except:
        print("^^ Timeout Error ^^")

dir = ['front', 'left', 'right', 'back', 'stop', 'none']
dir_ln = [0, 0, 0, 0, 0, 0]


def direc(f):
    cnt = 0
    start = 0
    r, r1 = 1, 1
    ln = 1
    sm = 0
    for i in f:
        if 255 in i:
            ind = np.where(i==255)
            sm += (ind[0][0]+ind[0][-1])//2
            if cnt==0:
                ln = len(ind[0])
                start = (ind[0][0]+ind[0][-1])//2
                r1 = r
                cnt = 1
            ln1 = len(ind[0])
            if ln1 > 3*ln:
                mid = (ind[0][0]+ind[0][-1])//2
                # p1 = (100+start, 50+r1)
                # p2 = (100+mid, 50+r)
                p1 = (100+((start*200)//60),50+((r1*200)//60))
                p2 = (100+((mid*200)//60),50+((r*200)//60))
                # cv2.line(frame1, p1, p2, (0,0,0), 2)
                # cv2.putText(frame1, 'Start', p1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,250), 2, cv2.LINE_AA)
                # angle = abs(round(atan2(p1[1]-p2[1], p1[0]-p2[0])*(180/pi), 2))
                dist = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
                return dist
        r+=1
    return 0.0


vid = cv2.VideoCapture(0)
cnt = 0
prev_command = 'none'
while True:
    _ , frame = vid.read()
    frame = cv2.flip(frame,2)

    cv2.rectangle(frame,(100,50),(300,250),(0, 0, 0),2)
    
    f = frame[50:251,100:301]
    f = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    f= cv2.resize(f, (60,60))
    
    # f = np.array(f, dtype=np.float64)
    # f[:,:,1] = f[:,:,1]*1.25
    # f[:,:,1][f[:,:,1]>255]=255
    # f[:,:,2] = f[:,:,2]*1.25
    # f[:,:,2][f[:,:,2]>255]=255
    # f = np.array(f, dtype=np.uint8)
    f2 = cv2.cvtColor(f, cv2.COLOR_HSV2BGR)
    f = cv2.medianBlur(f, 3)
    min_HSV = np.array([0, 30, 53]   , dtype = "uint8")      #[0, 10, 60]        [0, 58, 50]          [0, 30, 53]
    max_HSV = np.array([20, 150, 255], dtype = "uint8")   #[20, 150, 255]     [30, 255, 255]       [20, 150, 255]

    # min_ycrb = np.array([0,133,77],np.uint8)
    # max_ycrb = np.array([235,173,127],np.uint8)
    f = cv2.inRange(f, min_HSV, max_HSV)

    sm = 0
    
    f1 = f.copy()

    for k in range(1):
        r = 0
        for i in f[:-1]:
            if 255 in i:
                ind = np.where(i==255)[0]
                sm += ind.shape[0]
                for j in ind[:-1]:
                    f[r][j-1]=f[r][j+1]=f[r-1][j]=f[r-1][j-1]=f[r-1][j+1]=255
                    # f[r][j-1]=f[r-1][j]=f[r-1][j-1]=255
            r+=1
        # f = f[::-1]

    maxfing = 0
    for i in f[:25]:
        fing=0
        if 255 in i:
            ind = np.where(i==255)[0]
            ln = ind.shape[0]
            temp = 0
            for j in range(ln-6):
                if [ind[j], ind[j+1], ind[j+2], ind[j+3], ind[j+4], ind[j+5]] == [ind[j], ind[j]+1, ind[j]+2, ind[j]+3, ind[j]+4, ind[j]+5]:
                    temp += 1
                    fing += 1
            # print('temp',temp, ln)
            if temp + 6 == ln:
                # print('temp',temp, fing)
                break
        maxfing = max(maxfing, fing)

    # print("MAX FINGERS COUNT : ",maxfing)
    # print(sm)

    front = round(direc(f) , 2)
    left = round(direc(f.transpose()), 2)
    right = round(direc(f.transpose()[::-1]), 2)

    # print(front, left, right, maxfing, sep='\t')

    dir_dict = {front : 0, left: 1, right: 2}
    mx_dir = dir_dict[max(dir_dict)]
    
    if sm<300 or sm>1500 or max(dir_dict)==0 or maxfing>=21:
        dir_ln[5] += 1
        # print("none")
    elif maxfing>=7 and maxfing<=20:
        dir_ln[4] += 1
        # print("stop")
    elif maxfing in (2,3,4,5,6):
        dir_ln[3] += 1
        # print("back")
    else:
        dir_ln[mx_dir] += 1
        # print(dir[mx_dir])

    cv2.putText(frame, prev_command, (140, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,250), 2, cv2.LINE_AA)

    cnt += 1

    if cnt == 13:
        command = dir[dir_ln.index(max(dir_ln))]
        print(dir_ln)
        print(command)
        # cv2.putText(frame, command, (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,250,0), 2, cv2.LINE_AA)
        if command not in [prev_command, 'none']:
            send_command(command)
            prev_command = command

        cnt = 0
        dir_ln = [0, 0, 0, 0, 0, 0]

    cv2.imshow('Main Frame', frame)
    cv2.imshow('bg_frame', f)
    cv2.imshow('bg_frame1', f1)
    cv2.imshow('bg_frame2', f2)

    if cv2.waitKey(1) & (0XFF==ord('q') or 0XFF==ord('Q')):
        break

vid.release()
cv2.destroyAllWindows()

