from multiprocessing import Process, Event, Queue
import time
from ultralytics import YOLO
from mathfunc import line_func, dist_line_signed
from videoChannel import VideoChannel
from streamfunc import watchStream
import threading
from datab import update_db, check_cams, start_cams
import asyncio
from config import channels

#model = YOLO("yolov8n.pt") 
run = True
showVideo = False
selectedChannel = None
#psw = urllib.parse.quote("Wnidobrasil#22")
#video1 = cv2.VideoCapture(f'rtsp://admin:{psw}@192.168.24.37:554/media/video2')

psw1 = "Wnidobrasil#22"
psw2 = "admin"

#stream = {'ch1':objVideoChannel}

#





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

# Inicia a thread de escutprint(self.countAB)a
thread_console = threading.Thread(target=console)
thread_console.daemon = True
thread_console.start()


async def main():
    global run
    clock = True
    await start_cams(channels)

    last_time = time.time()
    last_time2 = time.time()

    while run:

        if time.time() - last_time > 1:
            last_time = time.time()
            #task1 = asyncio.create_task(check_cams())
            #task1.add_done_callback(lambda t: print(t.exception()))
            await check_cams()
        for key in channels:
            
            channel = channels[key]
            channel.analyse()
            if time.time() - last_time2 > 1:
                last_time2 = time.time()
                #task2 = asyncio.create_task(update_db(channel, key))
                #task2.add_done_callback(lambda t: print(t.exception()))
                await update_db(channel, key)
                #ab ba ponto

asyncio.run(main())