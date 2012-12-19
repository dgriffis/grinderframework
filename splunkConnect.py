#!/usr/bin/env python
from java.lang import *
from settings import getKeyValue
import com.splunk.Service as Service       
import com.splunk.Args as Args
import com.splunk.ResultsReaderXml as ResultsReaderXml
import sys

     
hostname = getKeyValue("splunk","splunk_host")
username = getKeyValue("splunk","username")
userpw = getKeyValue("splunk","password")
my_earliest_time = getKeyValue("splunk", "earliest_time")
my_latest_time = getKeyValue("splunk", "latest_time")
my_count = getKeyValue("splunk", "num_results")
my_search = getKeyValue("splunk", "search_query")
#print my_search
           
def splunkSearch(hostID):
    
    service = splunkConnect()
    
    oneshotSearchArgs = Args.create()
    #print "value for hostID is %s" % hostID
    if hostID == "nightlyTrend":
        oneshotSearchArgs.put("earliest_time", "-23h@h")
        oneshotSearchArgs.put("latest_time",   "now")
    else:      
        oneshotSearchArgs.put("earliest_time", my_earliest_time)
        oneshotSearchArgs.put("latest_time",   my_latest_time)
    oneshotSearchArgs.put("output_mode", "xml")
    oneshotSearchArgs.put("count", my_count)
    oneshotSearchQuery = my_search
    
    
    try:
        stream = service.oneshot(oneshotSearchQuery, oneshotSearchArgs)
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1
    
    return splunkResults(stream)

def splunkResults(stream):
        
    try:
        reader = ResultsReaderXml(stream)

    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1
       
    print "Retrieving data from splunk"
    searchFilters = []
    while True:
        try:
            myData = reader.getNextEvent()
            if myData:
                searchFilters.append(myData)
                #print myData
        except Exception, err:
            break
        
    reader.close()
 
    print "Splunk reader closed"   
    
    return searchFilters    
        

def splunkConnect():

    loginArgs = Args.create()
    loginArgs.add("host", hostname)

    print "Connecting to splunkSearch with login args of %s %s %s" % (loginArgs, username, userpw)

    try:
        service = Service.connect(loginArgs)
        service.login(username, userpw)

    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1
        
    return service
