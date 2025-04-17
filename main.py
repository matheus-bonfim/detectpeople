from multiprocessing import Process, Event, Queue
import time
import logging
from ultralytics import YOLO
from mathfunc import line_func, dist_line_signed
from videoChannel import VideoChannel
import urllib.parse
from streamfunc import watchStream
import cv2  
import threading

#model = YOLO("yolov8n.pt") 
run = True
showVideo = False
selectedChannel = None
#psw = urllib.parse.quote("Wnidobrasil#22")
#video1 = cv2.VideoCapture(f'rtsp://admin:{psw}@192.168.24.37:554/media/video2')

psw1 = "Wnidobrasil#22"
psw2 = "admin"

cam1 = {
    'name': 'ch1', 
    'url':'192.168.24.37:554/media/video2',
    'psw':psw1,
    'p1': (0, 500),
    'p2': (1280, 500)
}


cam2 = {
    'name': 'ch2',
    'url': '172.16.0.180/media/video1',
    'psw': psw2,
    'p1': (0, 420),
    'p2': (1037, 0)
}

cam3 = {
    'name': 'ch3',
    'url': '192.168.24.29:554',
    'psw': psw1,
    'p1': (0, 300),
    'p2': (1280, 400)}


cam4 = {
    'name': 'ch4',
    'url': '172.16.0.181/media/video1',
    'psw': psw2,
    'p1': (0, 450),
    'p2': (1280, 450)
}


streams_lst = [cam4, cam1]

channels = {}
channels_ret_frame = {}
#stream = {'ch1':objVideoChannel}

for stream in streams_lst:
    
    channels[stream['name']] = VideoChannel(stream['url'], stream['psw'], stream['p1'], stream['p2'])

def console():
    global showVideo, channels, run, selectedChannel
    while run:
        entrada = input().strip().lower().split()
        if not entrada:
            continue  # ignora entradas vazias
        
        comm = entrada[0]
        arg = entrada[1] if len(entrada) > 1 else None

        if comm == "w":
            if arg and arg in channels:
                selectedChannel = arg
                showVideo = True
            else:
                print("Canal não encontrado ou argumento ausente")
                
        elif comm == "q":
            run = False

        else:
            print(f"[Erro] Comando desconhecido: {comm}")

# Inicia a thread de escuta
thread_console = threading.Thread(target=console)
thread_console.daemon = True
thread_console.start()


last_time = time.time()
last_time2 = time.time()

while run:

    for key in channels:
        if time.time() - last_time > 0.0:
            last_time = time.time()
            channel = channels[key]
            ret, frame = channel.analyse()
            channels_ret_frame[key] = {'ret':ret, 'frame':frame}
            
        
    #print(channels_ret_frame)
    if showVideo:
        if selectedChannel:
            if time.time() - last_time > 0.03:
                last_time2 = time.time()
                ch = channels[selectedChannel]
                showVideo = watchStream(ch, channels_ret_frame[selectedChannel]['ret'], channels_ret_frame[selectedChannel]['frame'])
