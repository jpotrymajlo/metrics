# metrics

## Steps to run the script:

1) download the code from github
2) #cd metrics
3) #python3 -m venv .venv
4) #source .venv/bin/activate
5) #pip install -r requirements.txt
6) #python3 __main__.py filename

## Metrics
1) Number of events during a period of time
2) Number of host active during a periof of time
3) Percentage of time when particular hosts were active during a day - each hosts has its own number
4) Number of events outside regular working hours - each host has its own number
5) Number of events came from not allowed processes - at least one occurance should reise an alarm

In this script 1) and 2) are implemented.

## Alerts
1) Metric is larger then threshold if usually its value is lower
2) Metric is lower then threshold if usually its value is higer
3) Metric changes (detectng slopes)
4) Histogram changes
5) Peak detection - when metric has peaks alert should be raised

## Methods

1) To detect slope metric changes in time is filtered with low pass filter. Than the first and the second derivative is counted. After clipping we obtain peaks. Peaks indentify places that alarm shoould be raised. In this script alarms are represented by red dots.
2) Comparing values with the threshold - the easiest but not always proper method.
2) Changes of metric of histogram in the time can be represented as 1 or 2-dimensional signal. We can use FFT for analisys of the sigal.
3) AI - basing on history we can estimate 

The best way is to combine a few methods.
In this script the first method is used. I observed that sometimes peaks after first and second derivativse were not detected by peaks detection function. It shold be checked why. 
   
