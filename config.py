import queue

state = {'run': True, 'run_machine': True}
processes = {}
stop_events = {}
new_processes = queue.Queue()