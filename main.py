import os
pwdpath=os.getcwd()
from settings import *
from PIL import ImageGrab
if tsrf==True:
    from frontal_face import *
if not os.path.isfile(f'{pwdpath}/profiles/{person}/dclick.jpg'):
    from collect_data import *
else:
    if input('collect new data?(y/enter)')=='y':
        from collect_data import *
    else:pass
# data=['bros','up','down','left','right','dclick']
# color=[[0,0,0],[0,50,100],[100,50,0],[100,150,200],[200,150,100],[200,0,0]]
# thresholds=[.95,.85,.85,.85,.85,.9]
import math, time, cv2, pyautogui
import numpy as np
f_rate=[];x=[];locc=[]
pyautogui.FAILSAFE = False; pyautogui.PAUSE=0
enable=True;sizex,sizey=pyautogui.size()
cap = cv2.VideoCapture(0)
for i in range(len(data)):
    y = cv2.imread(f'{pwdpath}/profiles/{person}/{data[i]}.jpg',0)
    w, h = y.shape[::-1]
    x.append(y)
def tnsf(img,landmarks):
    images=[]
    marks,img=findc(img)
    i=0
    org=img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    for cls,x1,x2,y1,y2 in landmarks:
        if landmarks[i][0]=='bros':
            lx1=int(marks[x1][0]); lx2=int(marks[x2][0])
            ly1=int(marks[y1][1]);ly2=int((marks[landmarks[0][int(landmarks[0][4][0])]][1]+marks[landmarks[0][int(landmarks[0][4][2])]][1])/2)
            img=org[ly1-15:ly2+5,lx1-5:lx2+10]
            img=cv2.resize(img,(50,25))
#             img=img*(60/np.average(img));img=img.astype('uint8')
        elif landmarks[i][0]=='eye':
            lx1=int(marks[x1][0]); lx2=int(marks[x2][0])
            ly1=int(marks[y1][1]);ly2=int(marks[y2][1])
            img=org[ly1-10:ly2+10,lx1-10:lx2+15]
            img=cv2.resize(img,(50,25))
#             img=img*(60/np.average(img));img=img.astype('uint8')
#         img=cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
        images.append(img)
        if i==(len(data)-1):
            images=np.asarray(images,dtype=np.uint8)
        i+=1
    return images 
while 1:
    try:
        times=time.time()
        ret, img = cap.read()
        org=img = cv2.flip(img,1)
        if tsrf==False:
            img=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            images=[]
            for i in range(len(data)):
                images.append(img)
            images=np.asarray(images,dtype=np.uint8)
        if tsrf==True:
            images=tnsf(img,landmarks)
        for i in range(len(data)):
            prob = cv2.matchTemplate(images[i],x[i],cv2.TM_CCOEFF_NORMED)
#             print(np.average(images[i]))
            loc = np.where(prob >= thresholds[i])
            locc.append(loc)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(org, pt, (pt[0] + w, pt[1] + h), (color[i][0],color[i][1],color[i][2]), 2)
        if len(locc[0][0])>0:
            enable = not enable
            cap.set(cv2.CAP_PROP_BUFFERSIZE,1);ret, img = cap.read()
            print('enable:',enable)
            time.sleep(delay_after_dclick_or_enable);cap.set(cv2.CAP_PROP_BUFFERSIZE,4)
        mousex,mousey=pyautogui.position()
        box = (mousex-100,mousey-100,mousex+100,mousey+100)
        cursor=np.asarray(ImageGrab.grab(box),dtype=np.uint8)
        cursor=cv2.cvtColor(cursor,cv2.COLOR_BGR2RGB)
        cursor=cv2.resize(cursor,(120,120))
        cv2.imshow('cursoru',cursor);cv2.imshow('cursord',cursor);cv2.imshow('cursorl',cursor);cv2.imshow('cursorr',cursor)
        cv2.moveWindow('cursoru',int(sizex/2)-100,0)
        cv2.moveWindow('cursord',int(sizex/2)-100,sizey-120)
        cv2.moveWindow('cursorl',0,int(sizey/2)-100)
        cv2.moveWindow('cursorr',sizex-300,int(sizey/2)-100)
        if auto_correct_threshold==True:    
            if len(locc[1][0])>0 and len(locc[2][0])>0:
                if mousey<(sizey*auto_correct_up_pixel_limit) or mousey>(sizey*auto_correct_down_pixel_limit):
                    print('auto correcting threshold')
                    thresholds[1]=thresholds[1]+auto_threshold_correct_rate;thresholds[2]=thresholds[2]+auto_threshold_correct_rate
            if len(locc[3][0])>0 and len(locc[4][0])>0:
                if mousex<(sizex*auto_correct_left_pixel_limit) or mousex>(sizex*auto_correct_right_pixel_limit):
                    thresholds[3]=thresholds[3]+auto_threshold_correct_rate;thresholds[4]=thresholds[4]+auto_threshold_correct_rate
                    print('auto correcting threshold')
        if len(locc[1][0])>0 and enable:
#             print('up')
#             cv2.moveWindow('cursor',int(sizex/2)-20,0)
            for i in range(cursor_speed):
                pyautogui.move(0, -1)
        if len(locc[2][0])>0 and enable:
#             print('down')
#             cv2.moveWindow('cursor',int(sizex/2)-20,sizey-20)
            for i in range(cursor_speed):
                pyautogui.move(0, 1)
        if len(locc[3][0])>0 and enable:
#             print('left')
#             cv2.moveWindow('cursor',0,int(sizey/2)-20)
            for i in range(cursor_speed):
                pyautogui.move(-1, 0)
        if len(locc[4][0])>0 and enable:
#             print('right')
#             cv2.moveWindow('cursor',sizex-100,int(sizey/2))
            for i in range(cursor_speed):
                pyautogui.move(1,0)
        if len(locc[5][0])>0 and enable:
            pyautogui.doubleClick()
            print('dc')
            cap.set(cv2.CAP_PROP_BUFFERSIZE,1);ret, img = cap.read()
            time.sleep(delay_after_dclick_or_enable);cap.set(cv2.CAP_PROP_BUFFERSIZE,4)
        if tsrf==True:
            if show_left_eye==True:
                cv2.imshow('left eye',images[1])
            if show_left_eyebrow==True:    
                cv2.imshow('left eyebrow',images[0])
        if tsrf==False:
            cv2.imshow('org',org)
        if cv2.waitKey(1)==ord('c'):
            iput=input('which function is not working?(e/u/d/l/r/c):')
            for i in range(len(correct)):
                if iput==correct[i]:
                    undrovr=input('decrease or increase threshold?(d/i):')
                    if undrovr=='d':
                        thresholds[i]=thresholds[i]-threshold_correction_rate
                    if undrovr=='i':
                        thresholds[i]=thresholds[i]+threshold_correction_rate
            print(thresholds)
        f_rate.append(1/(time.time()-times))
        if print_frame_rate==True:
            print('fr:',1/(time.time()-times))
        if print_additive_average_frame_rate==True:
            print('afr:',sum(f_rate)/len(f_rate))
        locc=[]
    except Exception as a:
        print(a)