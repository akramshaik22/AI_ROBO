import cv2
vid = cv2.VideoCapture(0)

# dat = ['right', 'left', 'front', 'back', 'stop', 'none']
dat = ['none']
for i in dat:
    ret, frame = vid.read()
    # cv2.rectangle(frame,(100,50),(250,250),(0, 0, 0),2)
    # cv2.imshow('trail',frame)
    input(i)
    for j in range(3001):
        ret, frame = vid.read()
        frame=cv2.flip(frame,2)
        
        # cv2.imshow('Video', frame)
        # gr = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gr = frame
        cv2.rectangle(gr,(100,50),(300,250),(0, 0, 0),2)
        cv2.imshow('Video', gr)
        gr = gr[50:251,100:301]
        cv2.imwrite(f"D:/Programming/VS Code/Python/pdc/trainData/{i}/{str(j)}.jpg", gr)
        gr = cv2.cvtColor(gr, cv2.IMREAD_GRAYSCALE)
        cv2.imshow('ddd', gr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
vid.release()
cv2.destroyAllWindows()