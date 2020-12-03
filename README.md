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
I hit the ctrl-C, stopping the application, but not till it gracefully took and logged the last sample at: 1606754720

### The 'ts' variable is a unix epoch timestamp
Please see https://en.wikipedia.org/wiki/Unix_time and https://en.wikipedia.org/wiki/Coordinated_Universal_Time for background on the 'ts' variable. The first 'ts' is: *1606754706*, which is *2020-11-30T16:45:06+00:00* in time zone 0 (Greenwich, London UTC offset of 0)

### The 'apf' and 'bpf' variables:
Power factor in milli-units, divide by 1000 to obtain pf  
839 is a PF of .839 or arccos(.839) = 32.96 degrees

### The 'avoltage' and 'bvoltage' variables:
voltage in cV meaning, divide by 100 to obtain V  
12054 = 120.54 volts

### The acurrent and bcurrent variables:
current in mA, divide by 1000 to obtain Amps  
1200 = 1.2 amps

### The awattage and bwattage variables:
power is in watts
121 = 121 watts 

## log_eyedro.py details

log_eyedro.py is a python 3 application. You will likely need to install the requests module, to run this app. My development environments were Python 3.7.3 (debian container on chromebook metal & raspbian-debian on RPi hardware).  

### timing for, when the API obtains power data samples
The mytimer() function, sleeps, then returns, allowing the application to obtain power details via a restful API. If the API takes longer to process than the *sample_period* variable in the code, e.g. 2 seconds, mytimer() will hold-off for multiples of 2 seconds. My compute environments see ~3ms jitter-error, in the mytimer time-out, attributed to the operating system.

### restful API to post and obtain the power variables
The post_obtain_PfVIW() function executes a POST command to the eyedro web server's *:8080/getdata endpoint* e.g. 192.168.0.10:8080/getdata for my eyedro. If the POST is successful, returning a status = 200, the json dataset is returned as two python lists of variables, one for each power leg (left and right in the meter box, or red and black legs). one power leg list would look like and hold this: *[apf, avoltage, acurrent, awattage]* . In the event the POST application sees an error, takes longer to process or times-out, there will be no data points.

### main loop
The application continues to run, until the OS or the user interrupts or signals a kill. The application intercepts a kill signal, and completes the POST and writing the result to STDOUT, before gracefully exiting.

## getdata endpoint reliability
Have been running the API logging application from two Raspberry Pi's. The .3 IP addy PI is an old "RPI 2 model B rev1" board, one of the older PI boards. The .100 IP addy PI is a newer "RPI 3 model B Plus rev 1" board. Both RPIs are ethernet connected via short drop cables to the switch-router. 

On an older .3 IP RPI, competing for resources. When executing the POST getdata API endpoint every 2 seconds over a 3.5 hour period, the application captured 5160 2second (period) data points out of an expected 6435 data points. This is roughly an 80% success rate for 2 second captures. I also noted, when changing the platform running the POST, the eyedro could take +10 seconds to recover and start running successfully. Anecdotally, 1 second captures are even more error prone. I'll gather more stats on POST success.

12-01-2020 morning update ... over night, at a 4 second period sample time, running the app for 7628 seconds yielded 1783 data points but it should have held 1907 data points. the getdata success was 93.49%. this older RPI was also doing some production web scraping, so the getdata app was competing for compute. will try the newer RPI, that is not running apps.

12-01-2020 afternoon update ... ran the POST getdata API on the .100 RPI, without competing applications. running the app at 2 second sample period, for 6276 seconds yielded 3077 out of 3138 datasets ... successful at 98% ... POST failed or most likely, the POST took more than 2 seconds. initial take-away is; competing applications are a problem.

12-03-2020 mid morning update ... ran the POST getdata API on the .100 RPI, without competing applications. running the app at 2 second sample period for 59,835 elapsed seconds yielded 29918 potential data points, but we only captured 29261 data points. our success rate is 97.8 successful.

I'm starting to anayze the drop-outs for any time patterns.




