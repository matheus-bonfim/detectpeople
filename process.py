from multiprocessing import Process, Event
from videoChannel import VideoChannel
import time
from config import processes, stop_events, state, new_processes
from datetime import datetime, timedelta, date
import uuid

#channels[ponto] = VideoChannel(ponto, f'{ip}/media/video1', 'Wnidobrasil#22', p1, p2, countAB, countBA)

#[('ch1', '[66,275]', '[726,256]', None, None)]

def process_date(fromHour, toHour):
    
    daytoday = datetime.combine(datetime.today().date(), datetime.min.time())
    fromTime = daytoday + fromHour
    toTime = daytoday + toHour
    return fromTime, toTime



def create_channel_process(channel_info, psw, stop, data_queue):
    run = True
    print(channel_info)
    
    send_delay = 0.5
    last_time = time.time()
    ponto, p1, p2, ab, ba, rtsp_url, direction, tipo, fromTime, toTime = channel_info
    print(f'FromTime: {fromTime} toTime: {toTime}')
    
    channel = VideoChannel(ponto, rtsp_url, psw, p1, p2, ab, ba, tipo, direction=direction)
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
                
                id = str(uuid.uuid4())
                daytoday = datetime.now()
                daytoday_ms = int(1000 * daytoday.timestamp())
                    
                if fromTime != None and toTime != None: #mysql armazena timestamp em segundos tbm
                    fromTime_a, toTime_a = process_date(fromTime, toTime)

                    if daytoday >= fromTime_a and daytoday <= toTime_a:
                        data = { "id": id, "ponto": ponto, "ab": last_ab, "ba": last_ba, "notify": True, "datetime": daytoday_ms  }    
                    else:
                        data = { "id": id, "ponto": ponto, "ab": last_ab, "ba": last_ba, "notify": False, "datetime": daytoday_ms }
                else:
                    data = { "id": id, "ponto": ponto, "ab": last_ab, "ba": last_ba, "notify": False, "datetime": daytoday_ms }
                data_queue.put(data)
            
                