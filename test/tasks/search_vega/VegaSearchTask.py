#!/usr/bin/python

from test.framework.Task import Task


from net.grinder.script import Test
#from net.grinder.common import Logger
from net.grinder.script.Grinder import grinder

import sys

from xmlrpclib import *
from xml.dom.minidom import parseString

def log(message):
    """Log to the console, the message will include the thread ID"""
    grinder.logger.info(message)
    

class VegaSearchTask(Task):

     
    def __init__(self):
        """Initialize properties of class"""
        Task.__init__(self)
        self.description = "Run a Vega Search"
        self.urlDict = {}
        self.taskId = Task.numberOfTasks


    def initializeTask(self):
        """Initializes Instance Variables for this class. This method will be called by the Scenario object that this task belongs to."""
        
        if(not self.urlDict.has_key("url0")):
            raise Exception(self.__class__.__name__ + ".urlDict is missing values for one or more of the following keys: [url0]. Please define them in the constructor for the parent Scenario.")
        else:
            self.parameters = \
            { "appQuery":
                {"query":"myQuery"}
            }
   
    def getProxy(self, url):
        log("in getProxy with url: %s" % url)
        try:
            s = ServerProxy(url)
            #log("have my Proxy")  
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
       
        #log("argString is : %s" % argString)
        args={}
        searchArIDs=[]
        
        argKeyValues = argString.split('|')  #should look like key:type:value
        for nameKeys in argKeyValues :
            #log("value string is %s " % nameKeys)
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
          
        return args
            
    def run(self):
        #log("in postQuery")
        try:
                 
            s = self.getProxy(url=self.urlDict["url0"])
            query = self.getQuery()
            log("searchFilter is : %s" % query)
            
            #query = """"Name:uchino",vega,[16],0,30,0,{'searchUserId':163,'consultCutoff':365},{}"""
            #query = """"healthcare claims",vega,[16],0,30,0,{'searchUserId':163,'consultCutoff':365},{}"""
            paramArr=[]
            paramArr = query.split('\t')
            
            args = self.buildArgs(paramArr[2])
           

            s.SimpleSearch.execute(paramArr[1],paramArr[0],[16],0,30,0,args,{})
       
            
        except:
            print "Service returned an error:", sys.exc_info()[0]
            

