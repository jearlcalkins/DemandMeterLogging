# DemandMeterLogging
## Log Demand Metering Data - powerfactor, voltage, current, wattage

I need to know all my appliance and device load demands, especially the appliances with transient startup loads. I purchased a WIFI based EYEFI power demand monitor from EYEDRO (https://eyedro.com/product/eyefi-2/), to find and monitor my total aggregated household loads. The EYEFI device monitors instantaneous V (voltage) and I (current) from two current taps (CT sensors) and calculates the Power Factor (PF) and W (true power). The EYEFI observed and derived variables are logged approximately every second to the Eyedro cloud infrastructure. The EYEFI device also acts as a web site, providing your local access to the instantaneous power variables.

For analytical purposes I need to capture *V, I, PF, W* instantaneous data points, for both 120V legs, with a unix epoch time stamp. Eyedro has provided javascript code to view the EYEFI device's power variables.
```bash
https://eyedro.com/eyefi-getdata-api-command-sample-code/ 
```

The javascript code provides a restful POST example, that executes the EYEFI *getdata* endpoint. I’ve written a python 3 application to use the EYEFI POST getdata endpoint.

The log_eyedro.py python 3 application implements an EYEFI restful API, allowing one to periodically obtain two legs of *V-I-PF-W* data, and log the data points with a time stamp to STDOUT. The STDOUT can be redirected to a file and analyzed or graphed later. The example runs on a linux and python 3 environment, on Raspberry Pi hardware or a Debian (buster) chromebook instance.
 
### Install the python requests module:
I suggest looking at this site: https://realpython.com/python-requests/ , for restful API background and “how-to” install the python 3 requests module.

### Pull down the log_eyedro.py code:
Using the download button, pull-down the code or a zip of this repository (https://github.com/jearlcalkins/DemandMeterLogging)

### How to start and continually run the logging application, to the screen:

Cmd line pass variable -i is the eyedro IP address
Cmd line pass variable -p is sample period in second, samples every 2 seconds
```bash
python3 log_eyedro.py -i 192.168.0.10 -p 2
```
You can hit *ctrl-C* and kill the application in an orderly manner

### How to stop the logging application:

You can also kill the application from another shell by:
```bash
pfkill -f log_eyedro.py
```

### How to start and continually log data to a data file, and leave running in the background:
```bash
python3 log_eyedro.py -i 192.168.0.10 -p 2 >> power.csv &
```
To stop the background application, you’ll need to use a kill command, e.g. pfkill -f log_eyedro.py

## What does the data look like?
The log_eyedro.py application, outputs a CSV (comma seperated variable) output to STDOUT, beginning with header defintions.

```bash
python3 log_eyedro.py -i 192.168.0.10 -p 2
'ts', 'apf', 'avoltage', 'acurrent', 'awattage', 'bpf', 'bvoltage', 'bcurrent', 'bwattage'
1606754706, 839, 12054, 1200, 120, 955, 12057, 16400, 1888
1606754708, 840, 12046, 1200, 120, 954, 12050, 16440, 1889
1606754710, 839, 12048, 1200, 120, 955, 12052, 16440, 1891
1606754712, 839, 12052, 1200, 120, 954, 12055, 16480, 1894
1606754714, 839, 12056, 1200, 120, 954, 12060, 16440, 1890
1606754716, 840, 12053, 1200, 120, 956, 12056, 16360, 1885
1606754718, 841, 12064, 1200, 121, 955, 12067, 16440, 1893
^C
1606754720, 839, 12052, 1200, 120, 955, 12056, 16400, 1888
```

### The 'ts' variable is a unix epoch timestamp. Please see https://en.wikipedia.org/wiki/Unix_time and https://en.wikipedia.org/wiki/Coordinated_Universal_Time for background on the 'ts' variable.

### The 'apf' and 'bpf' variables:
Power factor in milli-units, divide by 1000 to obtain pf

### The avoltage and bvoltage variables:
voltage in mV meaning, divide by 1000 to obtain V

### The acurrent and bcurrent variables:
current in mA, divide by 1000 to obtain Amps

### The awattage and bwattage variables:
power is in watts
