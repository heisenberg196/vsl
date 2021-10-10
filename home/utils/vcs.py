import cv2
import numpy as np
from time import sleep
import threading



class VehicleCount(object):
    largura_min=80
    altura_min=80 
    file = 'media/traffic-feed/video.mp4'
    offset=6 

    pos_linha=550 
    frame2 = None
    delay= 6 
    detec = []
    carros= 0
    subtracao = cv2.createBackgroundSubtractorMOG2()


    def __init__(self):
        self.cap = cv2.VideoCapture(self.file)
        (self.ret, self.frame1) = self.cap.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.cap.release()

    def pega_centro(self, x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx,cy

    def get_frame(self):
        image = self.frame1
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            ret , self.frame1 = self.cap.read()
            tempo = float(1/self.delay)
            sleep(tempo) 
            grey = cv2.cvtColor(self.frame1,cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey,(3,3),5)
            img_sub = self.subtracao.apply(blur)
            dilat = cv2.dilate(img_sub,np.ones((5,5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
            dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
            contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            cv2.line(self.frame1, (25, self.pos_linha), (1200, self.pos_linha), (255,127,0), 3) 
            for(i,c) in enumerate(contorno):
                (x,y,w,h) = cv2.boundingRect(c)
                validar_contorno = (w >= self.largura_min) and (h >= self.altura_min)
                if not validar_contorno:
                    continue

                cv2.rectangle(self.frame1,(x,y),(x+w,y+h),(0,255,0),2)        
                centro = self.pega_centro(x, y, w, h)
                self.detec.append(centro)
                cv2.circle(self.frame1, centro, 4, (0, 0,255), -1)

                for (x,y) in self.detec:
                    if y<(self.pos_linha+self.offset) and y>(self.pos_linha-self.offset):
                        self.carros+=1
                        cv2.line(self.frame1, (25, self.pos_linha), (1200, self.pos_linha), (0,127,255), 3)  
                        self.detec.remove((x,y))
                        print("car is detected : "+str(self.carros))        
            cv2.putText(self.frame1, "VEHICLE COUNT : "+str(self.carros), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
