from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot
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
            
            hostName = tokens[0]
            eventDate = datetime.strptime(tokens[1], '%d/%m/%Y %H:%M')
            processName = tokens[2]

            eventsInTime(hostName, eventDate, processName)
            hostsInTime(hostName, eventDate, processName)

    
    pyplot.plot(numberOfEventsInTime)
    pyplot.savefig(fileName + "1.png")

    pyplot.clf()

  
    #counting the first and the second derivative to check where alarm
    #should be raised
    pyplot.plot(numberOfHostsInTime)
    x = np.array(numberOfHostsInTime, dtype=np.float)
    z = np.diff(x)

    pyplot.plot(np.diff(z))
    pyplot.savefig(fileName + "2.png")
    
if __name__ == '__main__':
    main()
