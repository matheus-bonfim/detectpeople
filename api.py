from flask import Flask, request, jsonify
from config import processes, stop_events, state, new_processes
from videoChannel import killVideoChannel, killAllVideoChannels
import asyncio
from processfunc import kill_process, kill_all_processes, restart_process
from datab import set_channel_as_new
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/resume')
def resume_machine():
    print("Machine back to work")
    state["run_machine"] = True
    return 'Machine back to work'

@app.route('/stop')
def stop_machines():
    asyncio.run(kill_all_processes(stop_events, processes))

    #blablablablalaaaa
    return 'Machine stopped'

@app.route('/stopMachine', methods=["GET"])
def stop_machine():
    ponto = request.args.get("ponto", type=str)
    ret = asyncio.run(kill_process(ponto, stop_events, processes))
    if ret:
        return f'Machine {ponto} stopped to work'
    return f'Machine {ponto} is already disabled'

@app.route('/startMachine', methods=["GET"])
def start_machine(): #somente avisa que tem nova cam na area
    new_processes.put(1)
    return f'Machine starting'

@app.route('/restartMachine', methods=["GET"])
def restart_machine():
    ponto = request.args.get("ponto", type=str)
    zerar = request.args.get("zerar", type=str)
    if zerar == 'true':
        zerar = True
    else:
        zerar = False
    
    def async_run():
        asyncio.run(restart_process(ponto, stop_events, processes, zerar))
    t = threading.Thread(target=async_run)
    t.start()
    
    if zerar:
        return f'Machine and counter restarted'
    else:
        return 'Machine restarted'


#if __name__ == "__main__":
 #   app.run(port=5500, debug=True)



 