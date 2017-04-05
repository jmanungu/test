
# coding: utf-8

# In[1]:

import sys, os
import subprocess
from collections import OrderedDict

# Define the function SortByValue that takes a dictionary as input and sorts it by values (and not by its keys!!!)
def SortByValue(dict):
    return OrderedDict(sorted(dict.items(), reverse = True, key=lambda x: x[1]))

# Define the function CountOccurences which counts the number of mutiplicity (or number of times an element of a dictionary is repeated)
def CountOccurences(dict):
    return {x:dict.count(x) for x in dict}
# Define the function duplicates which return the indices of repeated elements in a list
def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

# FIle to open:
fullFile = "/Users/mkiveni/Desktop/DataScienceTraining/DataEngineerInsight/insight/log_input/testlog.txt"
data = open(fullFile, "r")

# Read the content of the file and put the output in a list
Data = []
for line in data:
    Data.append(line)        
data.close()
#
# To get all the list of all IP/HOST, we should should split the elements of the LIST of Data on white space:
# The bandwidth consumption is extrapolated from bytes sent over the network and the frequency by which they 
# were accessed.
# BusiestPeriod is most frequently visited 60-minute period
IPHostList = []
BusiestPeriod1 = []
byte = []
bandWidth = []
for k in Data:
    # IP/Host
    splitElementOnWhiteSpace = str.split(k)  
    IPHostList.append(splitElementOnWhiteSpace[0])
    #Bandwidth   
    if len(splitElementOnWhiteSpace) >= 10:
        # the byte may contains a character "-", which will make it hard to to get the summed bandwidth appropraite.
        # We should set this character to zero to avaoid an issue.
        character = splitElementOnWhiteSpace[9]
        if character == "-":
            character = "0"
            byte.append(character)
            bandWidth.append(splitElementOnWhiteSpace[6])
        else:
            byte.append(character)
            bandWidth.append(splitElementOnWhiteSpace[6])

    #BusiestPeriod
    BusiestPeriod1.append(splitElementOnWhiteSpace[3])


# Now, let's count the number of IP/HOST duplicates
IPHostSortedDict = CountOccurences(IPHostList)

# The output of this is a dictionary. It has keys and values. Use values to sort on IPHostSortedDict
IPHostSortedDictByValue = SortByValue(IPHostSortedDict)

# IP/HOST output file:
IPHostFile = open("/Users/mkiveni/Desktop/DataScienceTraining/DataEngineerInsight/insight/log_output/hosts.txt", "w")
count1 = 0
for k, v in IPHostSortedDictByValue.items():
    ipLine = str(k) + ", " + str(v) + "\n"
    IPHostFile.write(ipLine)
    count1 = count1 + 1
    if count1 > 10:
        break

IPHostFile.close()

# The bandwidth should be the sum of all the bytes for every single occurence that the network were accessed:
BandwidthListSortedDict = {}

for bandwdth in set(bandWidth):
    indices = duplicates(bandWidth, bandwdth)
    if indices != "":
        sum = 0
        for ind in indices:        
            sum = sum + int(byte[ind])        
        if len(bandwdth) > 1:
            BandwidthListSortedDict[str(bandwdth)] = sum
    
    
# Bandwidth consumption can be xtrapolated by the frequency they were accessed:
#BandwidthListSortedDict = CountOccurences(BandwidthList)

# Bandwidth output file:
BandwidthListSortedDictByValue = SortByValue(BandwidthListSortedDict)

BandwidthFile = open("/Users/mkiveni/Desktop/DataScienceTraining/DataEngineerInsight/insight/log_output/resources.txt", "w")
count2 = 0
for k, v in BandwidthListSortedDictByValue.items():
    bandwidthLine = str(k) + "\n"
    if len(k) > 1:
        BandwidthFile.write(bandwidthLine)
    count2 = count2 + 1
    if count2 > 10:
        break
BandwidthFile.close()

# Busiest Period: (let's remove the caractere """[""" at the begining of each elements of my BusiestPeriod1)
BusiestPeriod = []

for element in BusiestPeriod1:
    BusiestPeriod.append(element.replace("[",""))
    
# Count the number of time the network was busy in a given time stamp
BusiestPeriodCount = SortByValue(CountOccurences(BusiestPeriod))

# Sort the element of the dictionary BusiestPeriodCount by keys this time.
BusiestPeriodCountSorted = {}

for key in BusiestPeriodCount.keys():
    newElement = str(key) + " -400"
    BusiestPeriodCountSorted[newElement] = BusiestPeriodCount[key]

# Create hours.txt file to save the most busiest period:
busiestPeriodFile = open("/Users/mkiveni/Desktop/DataScienceTraining/DataEngineerInsight/insight/log_output/hours.txt", "w")

count3 = 0    
for k, v in BusiestPeriodCountSorted.items():
    busytime = str(k) + ", " + str(v) + "\n"
    busiestPeriodFile.write(busytime)
    count3 = count3 + 1
    if count3 > 10:
        break
busiestPeriodFile.close()  

# Failed access: they are identified the HTTP request response.
FailedRequests = []
for lines in Data:
    if "304 " in lines:
        FailedRequests.append(lines)

# Find IP and time stamp of failed requests
FailedRequestsIP = []
TimeStampOfFailedIP = []
for iline in FailedRequests:
    # Split the line (iline) based on white space
    s = str.split(iline)
    # The IP is the first element from the above split
    FailedRequestsIP.append(s[0])
    # The time stamp is the third element in the pslit
    ts = s[3]
    TimeStampOfFailedIP.append(int(ts[13:15])*60 + int(ts[16:18]) + int(ts[19:21])*(1/60))
    
# Time stamp for all attempted requests
TimeStampOfAllIP = []
for iline in Data:
    # Split the line (iline) based on white space
    s = str.split(iline)
    # The time stamp is the third element in the pslit
    ts = s[3]
    TimeStampOfAllIP.append(int(ts[13:15])*60 + int(ts[16:18]) + int(ts[19:21])*(1/60))
    
# Create blocked.txt file to save the most busiest period:
blockedRequests = open("/Users/mkiveni/Desktop/DataScienceTraining/DataEngineerInsight/insight/log_output/blocked.txt", "w")

# Detect IP with a least three failled attemps
it = 0
for ip in FailedRequestsIP:
    stampedtime = []
    for p in duplicates(FailedRequestsIP, ip):
        stampedtime.append(TimeStampOfFailedIP[p])
    if len(stampedtime)>4:
        if (stampedtime[4] - stampedtime[0])>5:
            blockedRequests.write(FailedRequests[it])
    it = it + 1   
blockedRequests.close()


# In[ ]:



