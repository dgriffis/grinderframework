#!/usr/bin/env python
import yaml

def getSettings():
    settings_file = open("settings.yaml", 'r')
    settings = yaml.load(settings_file)
    settings_file.close()
    return settings

def getKeyValue(myHive, myKey):
    settings = getSettings()
    value = ""    
    for (key, item) in settings.items():
        #print key
        if key == myHive:
            for i in item:
                #print i
                for k in i:
                    if k == myKey:
                        value = i[k]
                        break
                    
    return value

def main():
    print getKeyValue("splunk", "earliest_time")
                    
if __name__ == "__main__":
    main()   