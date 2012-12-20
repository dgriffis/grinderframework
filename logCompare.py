#!/usr/bin/env python

import optparse
import sys
import os

import unittest
from testscenarios import TestWithScenarios
import xmlrunner

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-b", "--beforeLog", action="store", type="string", dest="beforeLog", default="devNightly-0-data.log",help="name of grinder baseline run data.log file.")
    parser.add_option("-c", "--afterLog", action="store", type="string", dest="afterLog", default="devDeploy-0-data.log", help="name of grinder change run data.log file.")
    parser.add_option("-l", "--logDir", action="store", type="string", dest="logDir", default="/Users/dgriffis/grinder/MyTests/Search_xmlrpc/log/", help="directory containing grinder data.log files.")
    
    return parser
    
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

LogHeaders = enum('Thread', 'Run', 'Test', 'Start_time', 'Test_time', 'Errors') 
        
    
def buildArray(logDir, fileName):

    fileTarget = os.path.join(logDir, fileName)
    #print "Target file is %s" % fileTarget
    try:
        array = [ line.strip() for line in file(fileTarget) ]
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        sys.exit()
  
    return array    
               
def _buildScenarios( numoftests):
    #scenario =  [('Row1', dict(param='1')),
    #             ('Row2', dict(param='2'))
    #              ]
    scenario = []   
    for x in range(0, numoftests):
        scenarioName = "scenario_"+str(x)
        scenario.append( (scenarioName, dict(param=x) ))
   
    return scenario

class Test(TestWithScenarios):
    changeAr = []
    baselineAr = []
    parser = get_args()
    (options, args) = parser.parse_args()
    #print "arg values are %s" % args
    #print "options are %s" % options
    
    logDir = options.logDir
    #print "logdir is %s" % logDir 
    beforeLog = options.beforeLog
    #print "beforeLog is %s" % beforeLog 
    afterLog = options.afterLog
    #print "afterLog is %s" % afterLog
    baselineAr = buildArray(logDir, beforeLog)
    changeAr = buildArray(logDir, afterLog)
  
    scenarios = _buildScenarios( len(baselineAr) ) 
    #print scenarios
            
    def setUp(self):
        self.assertTrue( len(self.baselineAr) == len(self.changeAr) )
   
    def tearDown(self):
        pass

    def testLogFileTestRunTimesComparable(self):
        blLine = self.baselineAr[self.param]
        chLine = self.changeAr[self.param]
        blData = blLine.split(",")
        chData = chLine.split(",")
        testNum = blData[LogHeaders.Test]
        if testNum.strip() == "Test":          
            return
        blVal = int(blData[LogHeaders.Test_time])
        chVal = int(chData[LogHeaders.Test_time])
        if blVal == 0 and chVal == 0:
            return
            
        pctDiff = 100 - ( float(chVal) / float(blVal) * 100 ) if blVal > chVal else 100 - ( float(blVal) / float(chVal) * 100 )

        self.assertLessEqual( pctDiff , 50 )
                                
if __name__ == "__main__":

    jtlFolder = "/Users/Shared/Jenkins/Home/jobs/Search_xmlrpc/workspace/test-reports"
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #xmlrunner.XMLTestRunner(output=jtlFolder).run(suite)
    