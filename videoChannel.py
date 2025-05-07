from mathfunc import line_func, dist_line_signed
import cv2
import urllib.parse
from ultralytics import YOLO
import torch
import ast

class VideoChannel:
    #video = {name:name, URL: url}
    def __init__(self, url, psw, p_line1, p_line2, direction=True, roi=None, offset=20): # roi = (y1,y2,x1,x2)
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO("yolov8n.pt")  # ou yolov8n.pt, yolov8m.pt...
        self.model.to(device)  # Garante que está na GPU

        psw = urllib.parse.quote(psw)
        self.p_line1 = ast.literal_eval(p_line1)
        self.p_line2 = ast.literal_eval(p_line2)
        print(self.p_line1)
        print(self.p_line2)
        self.videoStream = cv2.VideoCapture(f'rtsp://admin:{psw}@{url}', cv2.CAP_FFMPEG)
        self.al, self.bl = line_func(self.p_line1[0], self.p_line1[1], self.p_line2[0], self.p_line2[1])

        self.roi = roi
        if self.roi:
            self.ry1, self.ry2, self.rx1, self.rx2 = self.roi
        self.offset = offset
        self.sideA_ids = set()
        self.sideB_ids = set()
        self.countAB = 0
        self.countBA = 0 
        self.direction = direction

    def readVideo(self):
        return self.videoStream.read()

    def analyse(self):
        self.ret, self.frame = self.readVideo()
        if self.ret:
            if self.roi:
                frameROI = self.frame[self.ry1:self.ry2, self.rx1:self.rx2]
            else:
                frameROI = self.frame      
            self.results = self.model.track(frameROI, persist=True, classes=[0])  # habilita rastreamento por ID

            if self.results[0].boxes.id is not None:
                for box, cls, track_id in zip(self.results[0].boxes.xyxy,
                                              self.results[0].boxes.cls,
                                              self.results[0].boxes.id):
                    if int(cls) != 0:  # só pessoa
                        continue

                    x1, y1, x2, y2 = map(int, box)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # centro do bounding box
                    if(self.roi):
                        cy += self.ry1

                    d = dist_line_signed(cx, cy, self.al, self.bl)
                    if(d < -self.offset): #ta do lado B
                        if int(track_id) not in self.sideB_ids:
                            # tenta remover do lado A
                            if int(track_id) in self.sideA_ids:
                                self.sideA_ids.remove(int(track_id))
                                self.countAB += 1    
                            self.sideB_ids.add(int(track_id))

                             # incrementa só uma vez por ID
                    elif(d > self.offset): #está do lado A
                        if int(track_id) not in self.sideA_ids:
                            if int(track_id) in self.sideB_ids:
                                self.sideB_ids.remove(int(track_id))
                                self.countBA += 1
                            self.sideA_ids.add(int(track_id))   
        return self.ret, self.frame
