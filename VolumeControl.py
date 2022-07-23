import cv2
import time
import numpy as np
import HandTrackingModule1 as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime =0
cap=cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

detector =htm.handDetector(detectionCon=0.9)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
volBar=400
vol=0



while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) !=0:
        #print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy= (x1+x2)//2,(y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length= math.hypot(x2-x1,y2-y1)
        print(length)

        #hand range 50- 300
        #vol range -65 - 0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)





        if length<100:
            cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0),cv2.FILLED)



    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img, f'FPS:{int(fps)}', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break