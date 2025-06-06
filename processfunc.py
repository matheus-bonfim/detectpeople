from datab import change_channel_state


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

