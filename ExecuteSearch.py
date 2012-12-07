from net.grinder.script.Grinder import grinder
from test.framework.Scenario import Scenario
from test.tasks.search_vega import VegaSearchTask
from splunkConnect import splunkSearch
from settings import getKeyValue

#import random

xmlrpc_search_url = getKeyValue("xmlrpc", "url")
#  Make a new scenario
#
myScenario = Scenario(("Vega Search"), {"url0":xmlrpc_search_url});

searchTask = VegaSearchTask.VegaSearchTask()

# Connect to splunk and get last 24 hours of queries
searchFilters = splunkSearch( )

#The following lines builds an array from project csv
#searchFilters = [ line.strip() for line in file('searchQueries.csv') ]

#searchFilters = [{"query":"\"nuclear\",\"vega\",[16], 0, 20, 0, {}, {}"},
#                {"query":"\"Name:uchino\",\"vega\",[16],0,30,0,{},{}"},
#                {"query":"Name:uchino,vega,[16],0,30,0,{'searchUserId':163,'consultCutoff':365},{}"}]
                 
setattr(searchTask, "searchFilters", searchFilters)

#print "Total lines is %d" % lineCount

def parameterizeSearch(self=searchTask):
    #print "in parameterizeSearch"
    #index = random.randrange(0,lineCount)
    #print "index is %d" % index
    searchFilter = self.searchFilters[self.index];
    #print "search Filter is %s" % searchFilter;
    #queryString = searchFilter["query"];
    #print "query string is %s" % queryString;
    self.parameters["appQuery"]["query"] = searchFilter;
    #print "returning from parameterizeSearch"
    
searchTask.setParameterizingMethodFor("run", parameterizeSearch)

myScenario.addTask(searchTask)


class TestRunner:
    def __init__(self):
        grinder.properties["grinder.runs"] = str(len(searchFilters))
        
    def __call__(self):
        myScenario.run()