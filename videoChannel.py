from mathfunc import line_func, dist_line_signed
import cv2
import urllib.parse
from ultralytics import YOLO
import torch
import ast
import time



def killAllVideoChannels(channels):
    for key in list(channels.keys()):
        channels[key].videoStream.release()
        del channels[key] 

def killVideoChannel(ponto, channels):
    print(f"Encerrando {ponto}")
    channels[ponto].videoStream.release()
    del channels[ponto]


class VideoChannel:
    #video = {name:name, URL: url}
    def __init__(self, ponto, rtsp_url, psw, p_line1, p_line2, countAB, countBA, tipo, direction=1, roi=None, offset=20): # roi = (y1,y2,x1,x2)
        self.r_tracker_int = 5 * 60
        self.l_time = time.time()
        WEB_FRAME_HEIGHT = 450
        WEB_FRAME_WIDTH = 800
        self.ponto = ponto
        #self.url = f'{ip}/media/video3'
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO("yolov8n.pt")  # ou yolov8n.pt, yolov8m.pt...
        self.model.to(device)  # Garante que está na GPU

        psw = urllib.parse.quote(psw)
        self.p_line1 = ast.literal_eval(p_line1)
        self.p_line2 = ast.literal_eval(p_line2)
   
        self.videoStream = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        #1920/1080p

        frame_width = self.videoStream.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_height = self.videoStream.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if(frame_width > WEB_FRAME_WIDTH):
            alfa = abs(frame_width/WEB_FRAME_WIDTH) 
            self.p_line1_n = [alfa * self.p_line1[0], alfa * self.p_line1[1]]
            self.p_line2_n = [alfa * self.p_line2[0], alfa * self.p_line2[1]]
        
        else:
            alfa = 1 / (abs(WEB_FRAME_WIDTH/frame_width))
            self.p_line1_n = [int(alfa * self.p_line1[0]), int(alfa * self.p_line1[1])]
            self.p_line2_n = [int(alfa * self.p_line2[0]), int(alfa * self.p_line2[1])]
        
        n_frame = [alfa * WEB_FRAME_WIDTH, alfa * WEB_FRAME_HEIGHT]
        offset_x, offset_y = int(n_frame[0] - frame_width), int(n_frame[1] - frame_height)
        offset_x, offset_Y = 0, 0
        self.al, self.bl = line_func(self.p_line1_n[0] - offset_x, self.p_line1_n[1] - offset_y, self.p_line2_n[0] - offset_x, self.p_line2_n[1] - offset_y)

        self.roi = roi
        if self.roi:
            self.ry1, self.ry2, self.rx1, self.rx2 = self.roi
        self.offset = offset
        self.sideA_ids = set()
        self.sideB_ids = set()
        self.countAB = countAB
        self.countBA = countBA 
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
            if(time.time() - self.l_time > self.r_tracker_int):
                self.l_time = time.time()
                self.model.tracker = None
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
