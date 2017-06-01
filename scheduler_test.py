# -*- coding: utf-8 -*-
"""
Created on Wed May 24 09:32:00 2017

@author: WZhao10
"""

import sched, time
s = sched.scheduler(time.time, time.sleep)
update_frequency = 10
def scheduler(sc, t_query, update_frequency): 
    t_query_next = t_query+update_frequency
    s.enterabs(t_query_next,1,scheduler,(sc,t_query_next,update_frequency))
    
    #scheduled actions
    delta_t = time.time()-t_query
    print "%d: %f" % (t_query, delta_t)


t_init = int(time.time())+5
print "initial time: %d" % t_init
s.enterabs(t_init, 1, scheduler, (s, t_init,update_frequency))

s.run()

#%%


