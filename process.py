from multiprocessing import Process, Event
from videoChannel import VideoChannel
import time


#channels[ponto] = VideoChannel(ponto, f'{ip}/media/video1', 'Wnidobrasil#22', p1, p2, countAB, countBA)

#[('ch1', '[66,275]', '[726,256]', None, None)]


def create_channel_process(channel_info, psw, stop, data_queue):
    run = True
    send_delay = 0.5
    last_time = time.time()
    ponto, p1, p2, ab, ba, ip = channel_info
    channel = VideoChannel(ponto, ip, psw, p1, p2, ab, ba)
    last_ab = ab
    last_ba = ba

    while run:
        if stop.is_set():
            channel.videoStream.release()
            print('processo encerrando')
            break

        channel.analyse()
        if(time.time() - last_time > send_delay):
            # verifica se ab e ba mudaram
            if(channel.countAB != last_ab or channel.countBA != last_ba):
                last_ab = channel.countAB
                last_ba = channel.countBA
                last_time = time.time()
                print("sending data")
                data = { "ponto": ponto, "ab": last_ab, "ba": last_ba }
                data_queue.put(data)
            else:
                print("nao mudou")