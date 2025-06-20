from datab import change_channel_state, set_channel_as_new
from config import new_processes

async def kill_all_processes(stop_events, processes):
    for key in list(processes.keys()):
        await kill_process(key, stop_events, processes)

async def kill_process(ponto, stop_events, processes):
    if(stop_events[ponto] and processes[ponto]):
        stop_events[ponto].set()
        processes[ponto].join()
        await change_channel_state(ponto, 3)
        return True
    return False

async def restart_process(ponto, stop_events, processes, zerar):
    await kill_process(ponto, stop_events, processes)
    await set_channel_as_new(ponto, zerar)
    new_processes.put(1)

