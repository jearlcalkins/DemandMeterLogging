# DemandMeterLogging
Log Demand Metering Data - powerfactor, voltage, current, wattage

I am going to purchase a power generator for my home. To size the generator, I need to know load demands, for all appliances and devices. I purchased a WIFI based EYEFI power demand monitor from EYEDRO (https://eyedro.com/product/eyefi-2/), to find all my loads. The EYEFI monitors instantaneous V (voltage) and I (current) from two current taps (CT sensors) and calculates the Power Factor (PF) and W (true power). The observed and derived variables are logged approximately every second to the Eyedro cloud infrastructure.

For analytical purposes I need to capture my own V, I, PF, W data, for both 120vac legs, with an epoch time stamp. Eyedro has provided javascript code to view the EYEFI variables. https://eyedro.com/eyefi-getdata-api-command-sample-code/

