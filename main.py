from multiprocessing import Process, Event, Queue
from queue import Empty
import time
from ultralytics import YOLO
from mathfunc import line_func, dist_line_signed
from videoChannel import VideoChannel
from streamfunc import watchStream
import threading
import asyncio
from datab import get_ready_streams, update_channel_db
from process import create_channel_process
from config import processes, stop_events, state, new_processes
from api import app

psw = 'Wnidobrasil#22'

async def update_data(data_queue):
    while True:
        try:
            data = data_queue.get_nowait()
            await update_channel_db(data["ponto"], data["ab"], data["ba"])

        except Empty: #se nao tem nada na fila da exception
            break

async def check_and_create_process(new_processes, processes, stop_events, data_queue):
    try:
        new_processes.get_nowait()
        ch_list = await get_ready_streams(firstTime=False)
        for ch_info in ch_list:
            stop = Event()
            p = Process(target=create_channel_process, args=(ch_info, psw, stop, data_queue))
            p.start()
            processes[ch_info[0]] = p
            stop_events[ch_info[0]] = stop
            
    except Empty:
        return

async def main():
    def run_flask():
        app.run(port=5500, debug=False, use_reloader=False)

    thread_flask = threading.Thread(target=run_flask)
    thread_flask.start()

    ch_list = await get_ready_streams()


    data_queue = Queue()

    #def create_process():


    for ch_info in ch_list:
        stop = Event()
        p = Process(target=create_channel_process, args=(ch_info, psw, stop, data_queue))
        processes[ch_info[0]] = p
        stop_events[ch_info[0]] = stop
        p.start()

    #time.sleep(10)
    
    #atualiza dados no banco
    last_time = time.time()
    last_time_end = time.time()

    while state['run']:


        if( time.time() - last_time > 1):
            last_time = time.time() # bom criar threads para update_data
            await update_data(data_queue)
            await check_and_create_process(new_processes, processes, stop_events, data_queue)
            
    for key in list(processes.keys()):
        stop_events[key].set()
        processes[key].join()


if __name__ == "__main__":
    asyncio.run(main())
