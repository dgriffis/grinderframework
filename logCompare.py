#!/usr/bin/env python
import math
import optparse
import sys

import unittest
from xml.dom.minidom import parseString
import xmlrunner

#The only change should be the Qtime - any other change should be investigated
rspByteWarnAt = 1

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-b", "--beforeLog", action="store", type="string", dest="beforeLog", default="before-0-data.log",help="name of grinder baseline run data.log file.")
    parser.add_option("-c", "--afterLog", action="store", type="string", dest="afterLog", default="after-0-data.log", help="name of grinder change run data.log file.")
    parser.add_option("-l", "--logDir", action="store", type="string", dest="logDir", default="/Users/dgriffis/grinder/MyTests/Search_xmlrpc/log/", help="directory containing grinder data.log files.")
    
    return parser
    
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

LogHeaders = enum('Thread', 'Run', 'Test', 'Start_time', 'Test_time', 'Errors') 
        
    
def buildArray(logDir, fileName):
    fileTarget = logDir + fileName
    print "Target file is %s" % fileTarget

    try:
        array = [ line.strip() for line in file(fileTarget) ]
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        sys.exit()
  
    return array    

def compareRow(blRow,chRow):
    blData = blRow.split(",")
    chData = chRow.split(",")
    testNum = blData[LogHeaders.Test]
    if testNum.strip() == "Test":
        return
    
    #Compare response length
    if blData[LogHeaders.HTTP_response_length] != chData[LogHeaders.HTTP_response_length]:
        diffVal = math.fabs(int(blData[LogHeaders.HTTP_response_length])-int(chData[LogHeaders.HTTP_response_length]))
        if diffVal > rspByteWarnAt:
            print "Warning::Output data is vastly different for test query %s before value is %s and new run value is %s and should be investigated." % (testNum, blData[LogHeaders.HTTP_response_length], chData[LogHeaders.HTTP_response_length])
        else:
            print "Info::Output data is different for test query %s before value is %s and new run value is %s." % (testNum, blData[LogHeaders.HTTP_response_length], chData[LogHeaders.HTTP_response_length])
    
    #Flag non-200 response codes 
    #print chData[LogHeaders.HTTP_response_code]
    if chData[LogHeaders.HTTP_response_code].strip() != "200":  
        print "Error::Comparison test query %s returned a questionable http code of %s and should be investigated." % (testNum, chData[LogHeaders.HTTP_response_code])
               
def runCompare(baselineAr,changeAr):
    for blLine, chLine in zip(baselineAr, changeAr): 
        compareRow(blLine, chLine)


class Test(unittest.TestCase):
    changeAr = []
    baselineAr = []
    
    def setUp(self):
        parser = get_args()
        (options, args) = parser.parse_args()
        #print "arg values are %s" % args
        #print "options are %s" % options
    
        self.logDir = options.logDir
        print "logdir is %s" % self.logDir 
        self.beforeLog = options.beforeLog
        print "beforeLog is %s" % self.beforeLog 
        self.afterLog = options.afterLog
        print "afterLog is %s" % self.afterLog 
        self.baselineAr = buildArray(self.logDir, self.beforeLog)
        self.changeAr = buildArray(self.logDir, self.afterLog)
    
    def tearDown(self):
        pass

    def testLogFileRanSameNumberofTests(self):
        self.assertTrue( len(self.baselineAr) == len(self.changeAr) )

    def testLogFileTestRunTimesComparable(self):
        numoftestfails = 0
        for blLine, chLine in zip(self.baselineAr, self.changeAr):
            blData = blLine.split(",")
            chData = chLine.split(",")
            testNum = blData[LogHeaders.Test]
            if testNum.strip() == "Test":          
                continue
            blVal = int(blData[LogHeaders.Test_time])
            chVal = int(chData[LogHeaders.Test_time])
            if blVal == 0 or chVal == 0:
                continue
            
            pctDiff = 100 - ( float(chVal) / float(blVal) * 100 ) if blVal > chVal else 100 - ( float(blVal) / float(chVal) * 100 )

            try:
                self.assertLessEqual( pctDiff , 50 )
                
            except:
                numoftestfails+=1
                print "Failed Tests is %d with a pctDiff of %d - this test run is %s with a baseline of %d and comparison of %d"  % (numoftestfails, pctDiff, blData[LogHeaders.Run], blVal, chVal)
                continue
                
if __name__ == "__main__":
    unittest.main( testRunner=xmlrunner.XMLTestRunner(output='/Users/Shared/Jenkins/Home/jobs/Search_xmlrpc/workspace/test-reports') )
    
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    