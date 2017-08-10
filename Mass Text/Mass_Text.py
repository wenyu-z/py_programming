# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:28:03 2016

@author: Wenyu
"""

from subprocess import Popen, PIPE
import pandas as pd
import time

ewons = pd.read_csv('my_ewons.csv')

daynow = time.localtime().tm_mday
while time.localtime().tm_mday<=daynow+1:

    for pn in ewons.Phone:
        
        time.sleep(3)
        
        scpt = '''
            tell application "Messages"
                	set myid to get id of third service
                	set theBuddy to buddy "{}" of service id myid
                	send "goonline" to theBuddy
            end tell
            '''.format(pn)
        
        p = Popen('osascript', stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(scpt)
        print pn
        print (p.returncode, stdout, stderr)
        


        