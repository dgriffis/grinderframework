#!/usr/bin/python

from test.framework.Task import Task
from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from UserDict import UserDict

import sys

from xmlrpclib import *
from xml.dom.minidom import parseString

def log(message):
    """Log to the console, the message will include the thread ID"""
    grinder.logger.info(message)

DATE = 0
RESULT = 1
ELAPSED = 2
XML_SIZE = 3
APP_ID = 4
TOTAL_RESULTS = 5
QUERY = 6
START_INDEX = 7
MAX_RESULTS = 8
SORT_ORDER = 9
OBJECT_TYPES = 10
NAMED_ARGUMENTS = 11

def toIntArray(s):
    if len(s) > 0:
        return [int(x) for x in s.split(',')]
    else:
        return None

def toInt(s):
    if len(s) > 0:
        return int(s)
    else:
        return None

def toBoolean(s):
    if s == '' or s == 'false':
        return False
    else:
        return True

def toString(s):
    return s


class VegaSearchTask(Task):

    def __init__(self):
        """Initialize properties of class"""
        Task.__init__(self)
        self.description = "Run a Vega Search"
        self.urlDict = {}
        self.taskId = Task.numberOfTasks
        self.index = 0
        self.testRun = ""
        self.nFaults = 0
        self.hostID = grinder.properties["grinder.hostID"]
        if self.hostID == "prodNightly":
            logDir = grinder.properties["grinder.logDirectory"]
            targetFile = logDir+"/query.txt"
            self.myQueryFile = open(targetFile, "w")
            self.myQueryFile.close()
            
    def initializeTask(self):
        """Initializes Instance Variables for this class. This method will be called by the Scenario object that this task belongs to."""
        
        if(not self.urlDict.has_key("url0")):
            raise Exception(self.__class__.__name__ + ".urlDict is missing values for one or more of the following keys: [url0]. Please define them in the constructor for the parent Scenario.")
        else:
            self.parameters = \
            { "appQuery":
                {"query":"myQuery"}
            }

    def writeToFile(self, text):
        #print "Writing query %d" % self.index 
        
        filename = "%s-%d-page.xml" % ("xmlrpcSearch", grinder.runNumber)
        logDir = grinder.properties["grinder.logDirectory"]
        targetFile = logDir+"/"+self.hostID+"/"+filename
        #print "Log folder and filename is %s" % logDir+"/"+hostID+"/"+filename
        try:     
            myFile = open(targetFile, "w")
            s = text.encode('utf-8')
            print >> myFile, s
            myFile.close()
        except Exception, err:
            log('ERROR: %s\n' % str(err))  
  
    def writeSavedQuery(self, query):
        #print "Saving query %d" % self.index 
         
        logDir = grinder.properties["grinder.logDirectory"]
        targetFile = logDir+"/query.txt"
        try:   
            self.myQueryFile = open(targetFile, "a")
            print >> self.myQueryFile, query.encode('utf-8')
            self.myQueryFile.close()
        except Exception, err:
            log('ERROR: %s\n' % str(err))        
                    
    def getProxy(self, url):
        #log("in getProxy with url: %s" % url)
        try:
            s = Test(self.index, "xmlrpc search").wrap(ServerProxy(url, None))
        except:
            print "Service returned an error:", sys.exc_info()[0]
           
        return s

    def getQuery(self):
        #log("in getQuery")

        #log("before parameterizer")
        self.callParameterizingMethodFor("run")
        #log("after parameterizer")
                
        query = self.parameters["appQuery"]["query"]
        
        #log("searchFilter is : %s" % query)
    
        return query
    
    def buildArgs(self, argString):
       
        args={}
        searchArIDs=[]
        #print "argString is %s" % argString
        
        argKeyValues = argString.split('|')  #should look like key:type:value
        for nameKeys in argKeyValues :
            #print "value string is %s " % nameKeys
            namekeyVals = nameKeys.split(':')
            if namekeyVals[1]== 'I' :
                args[namekeyVals[0]]= int(namekeyVals[2])
            elif namekeyVals[1]== 'A' :
                valAr=namekeyVals[2].split(',')
                for valArVals in valAr :
                    if valArVals != '' :
                        searchArIDs.append(int(valArVals))
                        args[namekeyVals[0]]=searchArIDs
            elif namekeyVals[1]== 'B' :
                if namekeyVals[2] == "true":
                    args[namekeyVals[0]]= True
                else:
                    args[namekeyVals[0]]= False    
            else:
                args[namekeyVals[0]]= namekeyVals[2]
                
        #print "returning from buildArgs"  
        return args
            
    def run(self):
        #print "in postQuery"
        try:
            
            myterm = self.getQuery() 
            if self.hostID == "prodNightly":       
                lines = myterm["_raw"]
                """ term may contain multiple queries - we just want 1 """
                query = lines.split("\n")[0]
            else:
                query = myterm
            #print "The length after raw of lines is %d" % len(lines)   
            #print "VegaSearchTask query is : %s" % query     

            parts = query.strip().split("\t")
            if len(parts) < 3:
                self.index+=1
                return
        
            if "glgkeynote" in parts[QUERY].decode('utf-8').lower() or parts[QUERY].decode('utf-8').lower() == "technology" or parts[APP_ID] == "IndexSwitch":
                self.index+=1
                return
                         
            namedArgs = self.buildArgs(parts[NAMED_ARGUMENTS])
            testRun = self.getProxy(url=self.urlDict["url0"])
            
            #print '* DATE' + parts[DATE]
            #print '* RESULT' + parts[RESULT]
            #print '* ELAPSED' + parts[ELAPSED]
            #print '* XML_SIZE' + parts[XML_SIZE]
            #print '* APP_ID' + parts[APP_ID]
            #print '* TOTAL_RESULTS' + parts[TOTAL_RESULTS]
            #print '* QUERY' + parts[QUERY]
            #print '* START_INDEX' + parts[START_INDEX]
            #print '* MAX_RESULTS' + parts[MAX_RESULTS]
            #print '* SORT_ORDER' + parts[SORT_ORDER]
            #print '* OBJECT_TYPES' + parts[OBJECT_TYPES]
            #print '* NAMED_ARGUMENTS' + parts[NAMED_ARGUMENTS]
                        
            result = testRun.SimpleSearch.execute(parts[QUERY],
                                parts[APP_ID],
                                toIntArray(parts[OBJECT_TYPES].strip()),
                                0,
                                100,
                                int(parts[SORT_ORDER]),
                                namedArgs,
                                {})

            '''runs other than a prodNightly will execute queries from the saved query file - create the file here'''
            if self.hostID == "prodNightly":
                self.writeSavedQuery(query)
                   
            if self.hostID != "eclipse": 
                self.writeToFile(result)
                
            self.index+=1
        except:
            print "Service returned an error:", sys.exc_info()[0]
            log("fault on query %d with raw string of %s : " % ( self.index, query ))
            self.nFaults+=1
            self.index+=1

