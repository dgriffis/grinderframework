from net.grinder.script.Grinder import grinder
from test.framework.Scenario import Scenario
from test.tasks.search_vega import VegaSearchTask
from splunkConnect import splunkSearch
from settings import getKeyValue

hostID = grinder.properties["grinder.hostID"]
if "prod" in hostID:
    xmlrpc_search_url = getKeyValue("xmlrpc", "url1")
else:
    xmlrpc_search_url = getKeyValue("xmlrpc", "url0")

""" Make a new scenario """
myScenario = Scenario(("Vega Search"), {"url0":xmlrpc_search_url});
searchTask = VegaSearchTask.VegaSearchTask()

if hostID == "nightlyTrend":
    """ Connect to splunk and get last 24 hours of queries """
    searchFilters = splunkSearch( hostID )
else:
    """ Retrieve queries from the nightlyTrend saved query file """
    logDir = grinder.properties["grinder.logDirectory"]
    searchFilters = [ line.strip() for line in file(logDir+"/query.txt") ]
                 
setattr(searchTask, "searchFilters", searchFilters)


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