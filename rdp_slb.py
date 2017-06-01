# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:46:34 2016

@author: WZhao10
"""

import subprocess, webbrowser, json


webbrowser.open_new("https://fwauth.mgmt.slb.com")
#webbrowser.open("https://fwauth.mgmt.slb.com", new = 1, autoraise=False)

servers = {"a": "nl0123epc0580.dir.slb.com",
           "b": "nl0123epc0581.dir.slb.com",
           "c": "nl0123epc0330.dir.slb.com"}

print json.dumps(servers, indent=4, sort_keys=True)

sel = raw_input("Selection: ")
server_sel = servers[sel]

rdp = 'mstsc /v:' + server_sel
subprocess.Popen(rdp)


#%%

#import subprocess as sp
#import time
#def browse(url, how_long):
#    child = sp.Popen("start %s" % url, shell=True)
#    time.sleep(how_long)
#    child.kill()
#browse("https://fwauth.mgmt.slb.com", 3)



    
    
    