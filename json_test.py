# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:46:34 2016

@author: WZhao10
"""

import json

ddict = {'Wenyu':
			{'gender':'male',
			'favorite teams':{'soccer': 'Juventus',
								'football':'Patriots',
								'basketball':'Spurs',
								'baseball':'None',
								}}
		}

dd = json.dumps(ddict, indent=4)

#print dd
print ddict
print ddict['Wenyu']['favorite teams']['football']
