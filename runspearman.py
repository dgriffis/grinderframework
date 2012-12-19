#!/usr/bin/env python
import os
from xml.dom import minidom
import unittest
from testscenarios import TestWithScenarios
import xmlrunner

beforeFolder = '/Users/dgriffis/grinder/MyTests/Search_xmlrpc/log/nightlyTrend'
afterFolder = '/Users/dgriffis/grinder/MyTests/Search_xmlrpc/log/after'
tagValues = {"councilMemberResult":"councilMemberId", "clientContactResult":"PERSON_ID"}

def _getXMLText(element):
    nodelist = element.childNodes
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def _rank_dists(ranks1, ranks2):
    """Finds the difference between the values in ranks1 and ranks2 for keys
    present in both dicts. If the arguments are not dicts, they are converted
    from (key, rank) sequences.
    """
    ranks1 = dict(ranks1)
    ranks2 = dict(ranks2)
    for k, v1 in ranks1.iteritems():
        try:
            yield k, v1 - ranks2[k]
        except KeyError:
            pass

#@profile
def _spearman_correlation(ranks1, ranks2):
    """Returns the Spearman correlation coefficient for two rankings, which
    should be dicts or sequences of (key, rank). The coefficient ranges from
    -1.0 (ranks are opposite) to 1.0 (ranks are identical), and is only
    calculated for keys in both rankings (for meaningful results, remove keys
    present in only one list before ranking)."""
    n = 0
    res = 0
    #print ranks1
    #print ranks2
    ranks1 = sorted(ranks1, key=lambda k: -k[1])
    ranks2 = sorted(ranks2, key=lambda k: -k[1])

    ranks1 = [(t[0], ix) for ix, t in enumerate(ranks1)]
    ranks2 = [(t[0], ix) for ix, t in enumerate(ranks2)]

    for k, d in _rank_dists(ranks1, ranks2):
        res += d * d
        n += 1
    try:
        return 1 - (6 * float(res) / (n * (n * n - 1)))
    except ZeroDivisionError:
        # Result is undefined if only one item is ranked
        return 0.0
 
def _buildRankArray( cms, tagName ):
    ranking = 1.0
    rank = []
    for i in cms:
        id = int(_getXMLText(i.getElementsByTagName(tagName)[0]))
        rank.append((id,ranking))
        ranking+=1.0
        
    return rank
  
def _getTagItems(results, tagItem):
  
    return results[0].getElementsByTagName(tagItem)  

def _buildRanksArrays(which, testFile):
    #print testFile
    ranks = [(0,0), (1,1)]
    
    folder = beforeFolder
    if which == 2:
        folder = afterFolder
    xmldoc = minidom.parse( os.path.join(folder, testFile ) )
    results = xmldoc.getElementsByTagName("results")
    
    if int(results[0].getAttribute("count"))<2:
        return ranks
    
    '''search will return results tagged as councilMemberResult or clientContactResult '''
    tagName=''
    cms=''
    for key in tagValues.keys():
        tagItem = key
        tagName = tagValues[key]
        cms = _getTagItems(results, tagItem)
        if len(cms) > 0:
            break

    if len(cms) == 0:
        return ranks
         
    ranks1 = _buildRankArray(cms, tagName)
    #print ranks1
  
    return ranks1
    
def _buildScenarios(): 
    
    #scenario =  [('scenariotest1', dict(param='xmlrpcSearch-0-page.xml')),
    #              ('scenariotest2', dict(param='xmlrpcSearch-1-page.xml'))
    #              ]
    scenario = []   

    for r,d,f in os.walk(beforeFolder):
        for myFile in f:
            scenario.append( (myFile, dict(param=myFile) ))

    return scenario   
 
class Test(TestWithScenarios):
    
    ranks1 = []
    ranks2 = []
    scenarios = _buildScenarios()   
      
    def setUp( self ):
        #print 'param=', self.param
        self.ranks1 = _buildRanksArrays( 1, self.param )
        self.ranks2 = _buildRanksArrays( 2, self.param )
        
    def tearDown(self):
        pass
    
    def testSpearmanCoefficient(self):    
        result = _spearman_correlation(self.ranks1, self.ranks2)
        #print "spearman result is %f" %  result
        self.assertTrue( result == 1.0 )
        #print "spearman for file %s is %f" % ( self.param, result )  
    
if __name__ == '__main__':  
   
    #ranks1 = []
    #ranks2 = []
    #ranks1= [('a', 2.5), ('b', 3.5), ('c', 3.0), ('d', 3.5)]
    #ranks2= [('c', 3.5), ('b', 4.5), ('e', 1.0), ('d', 1.5)]
    #ranks1= [(219378, 1.0), (510847, 2.0), (489352, 6.0), (215446, 5.0), (166881, 3.0), (418280, 4.0), (256081, 7.0), (248372, 8.0)]
    #ranks2= [(219378, 6.0), (510847, 1.0), (489352, 3.0), (215446, 4.0), (166881, 5.0), (418280, 3.0), (256081, 2.0), (248372, 7.0)]
    #print spearman_correlation(ranks1, ranks2)  

    suite = unittest.TestLoader().loadTestsFromTestCase(Test)            
#    unittest.TextTestRunner(verbosity=2).run(suite)  
    xmlrunner.XMLTestRunner(output='/Users/Shared/Jenkins/Home/jobs/runspearman/workspace/test-reports').run(suite)