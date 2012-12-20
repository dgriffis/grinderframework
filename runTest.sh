#!/bin/sh

if [ $# -eq 0 ]
then
    echo "Usage : $0 runtype[prodNightly,prodDeploy,devNightly,devDeploy]"
    exit
fi


case "$1" in

'prodNightly')  echo "Nightly prod trending"
hostID="prodNightly"
;;
'prodDeploy')  echo  "Deploy prod"
hostID="prodDeploy"
;;
'devNightly')  echo  "Nightly development trending"
hostID="devNightly"
;;
'devDeploy') echo  "Deploy development"
hostID="devDeploy"
;;
*) echo "Default: Nightly prod trending"
hostID="prodNightly"
;;
esac



echo "Deleteing test output files"
pushd log/$hostID
rm *.xml
popd

echo "Running test"

/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/bin/java -classpath /Users/dgriffis/jython2.5.2/jython.jar:/Users/dgriffis/grinder/MyTests/Search_xmlrpc:/Users/dgriffis/grinder/lib/grinder.jar:/Users/dgriffis/splunk/dist/splunk-external.jar:/Users/dgriffis/splunk/dist/splunk-sdk.jar:/Users/dgriffis/splunk/dist/splunk.jar:/Applications/eclipse/plugins/org.python.pydev_2.6.0.2012062818/pysrc/pydev_sitecustomize:/Users/dgriffis/grinder/MyTests/Search_xmlrpc:/Users/dgriffis/grinder/lib/grinder.jar:/Users/dgriffis/splunk/dist/splunk-external.jar:/Users/dgriffis/splunk/dist/splunk-sdk.jar:/Users/dgriffis/splunk/dist/splunk.jar:/Users/dgriffis/jython2.5.2/Lib:/Users/dgriffis/jython2.5.2/Lib/site-packages:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/classes.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/ui.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/jsse.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/jce.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/charsets.jar:/System/Library/Java/Extensions/AppleScriptEngine.jar:/System/Library/Java/Extensions/dns_sd.jar:/System/Library/Java/Extensions/j3daudio.jar:/System/Library/Java/Extensions/j3dcore.jar:/System/Library/Java/Extensions/j3dutils.jar:/System/Library/Java/Extensions/jai_codec.jar:/System/Library/Java/Extensions/jai_core.jar:/System/Library/Java/Extensions/mlibwrapper_jai.jar:/System/Library/Java/Extensions/MRJToolkit.jar:/System/Library/Java/Extensions/QTJava.zip:/System/Library/Java/Extensions/vecmath.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/apple_provider.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/dnsns.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/localedata.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/sunjce_provider.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/sunpkcs11.jar:/Library/Python/2.7/site-packages/yaml:/Library/Python/2.7/site-packages -Dpython.path=/Users/dgriffis/grinder/MyTests/Search_xmlrpc:/Users/dgriffis/grinder/lib/grinder.jar:/Users/dgriffis/splunk/dist/splunk-external.jar:/Users/dgriffis/splunk/dist/splunk-sdk.jar:/Users/dgriffis/splunk/dist/splunk.jar:/Applications/eclipse/plugins/org.python.pydev_2.6.0.2012062818/pysrc/pydev_sitecustomize:/Users/dgriffis/grinder/MyTests/Search_xmlrpc:/Users/dgriffis/grinder/lib/grinder.jar:/Users/dgriffis/splunk/dist/splunk-external.jar:/Users/dgriffis/splunk/dist/splunk-sdk.jar:/Users/dgriffis/splunk/dist/splunk.jar:/Users/dgriffis/jython2.5.2/Lib:/Users/dgriffis/jython2.5.2/Lib/site-packages:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/classes.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/ui.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/jsse.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/jce.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Classes/charsets.jar:/System/Library/Java/Extensions/AppleScriptEngine.jar:/System/Library/Java/Extensions/dns_sd.jar:/System/Library/Java/Extensions/j3daudio.jar:/System/Library/Java/Extensions/j3dcore.jar:/System/Library/Java/Extensions/j3dutils.jar:/System/Library/Java/Extensions/jai_codec.jar:/System/Library/Java/Extensions/jai_core.jar:/System/Library/Java/Extensions/mlibwrapper_jai.jar:/System/Library/Java/Extensions/MRJToolkit.jar:/System/Library/Java/Extensions/QTJava.zip:/System/Library/Java/Extensions/vecmath.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/apple_provider.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/dnsns.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/localedata.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/sunjce_provider.jar:/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home/lib/ext/sunpkcs11.jar:/Library/Python/2.7/site-packages/yaml:/Library/Python/2.7/site-packages -Dgrinder.script=/Users/dgriffis/grinder/MyTests/Search_xmlrpc/ExecuteSearch.py -Dgrinder.hostID=$hostID net.grinder.Grinder /Users/dgriffis/grinder/MyTests/Search_xmlrpc/grinder.properties
