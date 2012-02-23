from test.framework.Scenario import Scenario
from test.tasks.search_vega import VegaSearchTask
import random

#
#  Make a new scenario
#

myScenario = Scenario(("Vega Search"), {"url0":"http://10.143.1.7:9008/xmlrpc"});
searchTask = VegaSearchTask.VegaSearchTask()

searchFilters = []
lineCount = 0
for line in file('searchQueries.csv'):
    searchFilters.append(line.strip())
    lineCount+=1

#searchFilters = [{"query":"\"nuclear\",\"vega\",[16], 0, 20, 0, {}, {}"},
#                {"query":"\"Name:uchino\",\"vega\",[16],0,30,0,{},{}"},
#                {"query":"Name:uchino,vega,[16],0,30,0,{'searchUserId':163,'consultCutoff':365},{}"}]
                 
setattr(searchTask, "searchFilters", searchFilters)

#print "Total lines is %d" % lineCount

def parameterizeSearch(self=searchTask):
    #print "in parameterizeSearch"
    index = random.randrange(0,lineCount)
    #print "index is %d" % index
    searchFilter = self.searchFilters[index];
    #print "search Filter is %s" % searchFilter;
    #queryString = searchFilter["query"];
    #print "query string is %s" % queryString;
    self.parameters["appQuery"]["query"] = searchFilter;
    #print "returning from parameterizeSearch"
    
searchTask.setParameterizingMethodFor("run", parameterizeSearch)

myScenario.addTask(searchTask)


class TestRunner:
    def __call__(self):
        myScenario.run()