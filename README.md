# DemandMeterLogging
Log Demand Metering Data - powerfactor, voltage, current, wattage

I am going to purchase a power generator for my home, and to size the generator. I need to know all my appliance and device load demands, especially the appliances with transient startup loads. I purchased a WIFI based EYEFI power demand monitor from EYEDRO (https://eyedro.com/product/eyefi-2/), to find all my loads. The EYEFI device monitors instantaneous V (voltage) and I (current) from two current taps (CT sensors) and calculates the Power Factor (PF) and W (true power). The EYEFI observed and derived variables are logged approximately every second to the Eyedro cloud infrastructure. The EYEFI device also performs as a web site, providing local access to the instantaneous variables. 

For analytical purposes I need to capture my own V, I, PF, W instantaneous data, for both 120vac legs, with an epoch time stamp. Eyedro has provided javascript code to view the EYEFI device's variables. https://eyedro.com/eyefi-getdata-api-command-sample-code/ The javascript code provides a restful POST example, that runs against an EYEFI getdata endpoint. This POST getdata endpoint example is implemented in my python3 code example.

The log_eyedro.py python 3 application implements an EYEFI restful API, allowing one to periodically obtain V-I-PF-W data, and write a time stamp and data point to STDOUT. The STDOUT dataset can be redirected to a file.
