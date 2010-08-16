#!/usr/bin/env python2.6

import sys
import os
name='/data_pan2/xtalk_1_28_10_png/xtalk_auto_1_28_10_xtalk_'+sys.argv[1]+'_'+sys.argv[2]+'.png'
print name
os.system('gthumb '+name)


