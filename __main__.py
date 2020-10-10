from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot
from matplotlib import gridspec
from scipy.signal import find_peaks
from scipy.signal import lfilter
from scipy.signal import savgol_filter
from scipy.signal import argrelmax
import numpy as np
import sys


numberOfEvents = 0
numberOfEventsInTime = []
startTime1 = datetime.fromtimestamp(0)

# number of events received during 10 minutes 
def eventsInTime(hostName, eventDate, processName, period=timedelta(minutes=10)):
    global numberOfEvents
    global startTime1
    global numberOfEventsIntime

    if startTime1 == datetime.fromtimestamp(0):
        startTime1 = eventDate

    numberOfEvents += 1

    if eventDate - startTime1 > period:
        numberOfEventsInTime.append(numberOfEvents)
        numberOfEvents = 0
        startTime1 = eventDate

# number of host generating events during 10 minutes
hostsActivity = dict()
numberOfHostsInTime = []
startTime2 = datetime.fromtimestamp(0)

def hostsInTime(hostName, eventDate, processName, period=timedelta(minutes=10)):
    global hostsActivity
    global numberOfHostsInTime
    global startTime2

    if startTime2 == datetime.fromtimestamp(0):
        startTime2 = eventDate

    if hostName in hostsActivity:
        hostsActivity[hostName] += 1
    else:
        hostsActivity[hostName] = 1


    if eventDate - startTime2 > period:
        numberOfHostsInTime.append(len(hostsActivity))
        startTime2 = eventDate
        hostsActivity.clear()


def main ():
    if len(sys.argv) != 2:
        print("provide filename")
        return
    fileName = str(sys.argv[1])
    with open(fileName, 'r') as file:
        for line in file:
            tokens = line.split(',')
            try: 
                hostName = tokens[0]
                eventDate = datetime.strptime(tokens[1], '%d/%m/%Y %H:%M')
                processName = tokens[2]

                eventsInTime(hostName, eventDate, processName)
                hostsInTime(hostName, eventDate, processName)
            except:
                pass

    slopeAlert(numberOfHostsInTime, fileName + ".1.png", "Active hosts / " + str(10) + "min")
    slopeAlert(numberOfEventsInTime, fileName + ".2.png", "Events in / " + str(10) + "min")
    slopeAlertSavgolFilter(numberOfEventsInTime, fileName + ".3.png", "Savgol")

# detecting slopes using Savgol Filter
def slopeAlertSavgolFilter(data, fileName, title):
    x = np.array(data, dtype=np.float)

    fig = pyplot.figure() 
    grid = gridspec.GridSpec(5,1)
    plot0 = pyplot.subplot(grid[0])
    plot0.set_title(title)
    plot0.plot(x)

    res = savgol_filter(x, window_length=101, polyorder=2, deriv=2)
    #to do - this implementation doesn't give correct results
    #filtered is data are quite nice

    max_res = np.max(np.abs(res))
    large = np.where(np.abs(res) > max_res/2)[0]
    gaps = np.diff(large) > 101
    begins = np.insert(large[1:][gaps], 0, large[0])
    ends = np.append(large[:-1][gaps], large[-1])
    changes = ((begins+ends)/2).astype(np.int)

    plot1 = pyplot.subplot(grid[1])
    plot1.set_title("filtered")
    plot1.plot(res)

    plot2 = pyplot.subplot(grid[2])
    plot2.set_title("alerts")
    plot2.plot(changes, x[changes], 'ro')
    
    pyplot.tight_layout()
    pyplot.savefig(fileName)

    pyplot.clf()

def slopeAlert(data, fileName, title):

    x = np.array(data, dtype=np.float)

    fig = pyplot.figure() 
    grid = gridspec.GridSpec(5,1)
    plot0 = pyplot.subplot(grid[0])
    plot0.set_title(title)
    plot0.plot(data)
    
    #lowpassfilter. We are rathter interested in detecting slopes in this
    #detector
    n = 15
    b = [1.0/n]*n
    a = 1
    xx = lfilter(b,a,x)
    plot0.plot(xx)

    #calculate 1st and 2nd derivative to detect slopes
    firstD = np.diff(xx)
    secondD = np.diff(firstD)
    plot1 = pyplot.subplot(grid[1])
    plot1.set_title("2nd derivative")
    plot1.plot(secondD)

    #detecting local maximas and minimas
    clipped = np.clip(np.abs(np.gradient(secondD)), 0.3, 4)
    plot2 = pyplot.subplot(grid[2])
    plot2.set_title("smothed")
    plot2.plot(clipped)

#    max_idx = argrelmax(clipped)[0]
    max_idx, _ = find_peaks(clipped, height=0)
    plot3 = pyplot.subplot(grid[3])
    plot3.set_title("alerts")
    plot3.plot(max_idx, clipped[max_idx], 'ro')

    
    pyplot.tight_layout()
    pyplot.savefig(fileName)

    pyplot.clf()

if __name__ == '__main__':
    main()
