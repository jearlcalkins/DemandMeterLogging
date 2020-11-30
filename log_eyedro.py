import time
import requests
import signal
import argparse

sample_period = 2
eyedro_ip = '192.168.0.10'
api_endpoint_url = 'http://' + eyedro_ip + ':8080/getdata'
heading =['ts', 'apf', 'avoltage', 'acurrent', 'awattage', 'bpf', 'bvoltage', 'bcurrent', 'bwattage']

# pass arguements in the passline if helpful
# eyedro IP address is: 192.168.0.10 ... over ride with -i 192.168.0.100
# sample rate period is 2 second ... over over ride with -p 4 (4 second samples)
# python3 log_eyedro.py -i 192.168.0.100 -p 4
# python3 log_eyedro.py -h
varparse = argparse.ArgumentParser()
varparse.add_argument('-i', type=str, default=eyedro_ip, help="eyedro IP address")
varparse.add_argument('-p', type=int, default=sample_period, help="defines the eyedro sampling period (sec)")
args = varparse.parse_args()
eyedro_ip = args.i
sample_period = args.p

before = time.time()

# the NiceKiller class / object allows the application to intercept a ctrl-c or kill, complete an
# API post, write results, then shutdown nicely
class NiceKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_nicely)
        signal.signal(signal.SIGTERM, self.exit_nicely)

    def exit_nicely(self,signum, frame):
        self.kill_now = True
        
# the mytimer function, sleeps, wakes up, and returns when the next period-time comes about. 
# for example, if the period is 10 (seconds), and the UTC time is 1606687712, mytimer  will hang 
# until 1606687720. If the API runs after mytimer times-out, and it completes quickly and 
# correctly (http result of 200), then calling mytimer() again, the API will run again at: 1606687730
# if an API call runs slowly and takes more time than the period (e.g.10 seconds), calling
# mytimer will return at the next multiple time of 10 second e.g. 1606687730
# for my debian instance, running in a chromebook container, there is a roughly a 3ms jitter.
# when we should return at 1606687730, we more often see it return at 1606687730.003

def mytimer():
    nowf = time.time() 
    nowi = int(nowf)
    r = nowi % sample_period
    next = float(nowi + (sample_period - r))
    delta = next - nowf
    time.sleep(delta)
    after = time.time()
    return after

# the eyedro restful API post to the :8080/getdata endpoint yields data for the
# a) and the b) current taps
# an example of the returned API text response:
# {"data":[[850,12166,1160,119],[561,12168,720,48]]}
# the a) current tap provides
# pf = 850 = .850
# voltage = 12166 = 121.66 volts
# current = 1160 = 1.160 amps
# power = 119 = 119 watts

def post_obtain_PfVIW():
    result = True
    try:
        response = requests.post(url = api_endpoint_url)
    except requests.ConnectionError as error:
        result = False

    if result == True:
        if response.status_code == 200:
            json_stuff = response.json()
            power_stuff = json_stuff['data']
            a = power_stuff[0]
            b = power_stuff[1]
            status_code = response.status_code 
            # [apf, avoltage, acurrent, awattage] = a
            # [bpf, bvoltage, bcurrent, bwattage] = b
    else:
        a = []
        b = []
        status_code = ''

    return (result, status_code, a, b)

# the main loop continues as long as the OS or a user, has not signaled to kill
# the python PID process or kill the process with a ctrl-C
# the API endpoint is called every X seconds, where X is the sample period
# the main loop comes to an end, if it's received a kill signal, but it completes
# the post and writes data points to stdout (if post was successful) as CSV

def main():
    ctr = 0
    killer = NiceKiller()
    print(str(heading).strip('[]'))
    now = mytimer()

    while not killer.kill_now:
        ctr += 1
        (result, status_code, a, b)  = post_obtain_PfVIW()
        now = mytimer()
        if result :
            print("%10.0f" % now, end = ", ")
            print(str(a).strip('[]'), end = ", ")
            print(str(b).strip('[]'))
    print("")

if __name__ == "__main__":
    main()

