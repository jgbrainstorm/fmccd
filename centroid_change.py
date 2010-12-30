#! /usr/bin/env python
import numpy as np
import pyfits as pf
import scipy.ndimage as nd
import pylab as pl
import sys

ext=
def getxy(datas):
    ok=datas>=datas.mean()+datas.std()
    good=nd.binary_opening(ok,structure=np.ones((30,30)))    
    datagood=datas*good
    structuring_element=np.ones((3,3))
    segmentation,segments=nd.label(good,structure=structuring_element)    
    coords=nd.center_of_mass(datagood,segmentation,range(1,segments+1))
    xcoords=np.array([x[1] for x in coords])
    ycoords=np.array([x[0] for x in coords])
    return xcoords,ycoords

if len(sys.argv) == 1:
    print 'syntax: centroid_pos imageName1 imageName2'
else:
    data1,hdr1=pf.getdata(sys.argv[1],int(sys.argv[3]),header=True)
    pl.figure(figsize=(14,9))
    pl.subplot(2,2,1)
    x1,y1=getxy(data1,sys.argv[1]+'['+sys.argv[3]+']')
    pl.subplot(2,2,2)
    data2=pf.getdata(sys.argv[2],int(sys.argv[3]))
    x2,y2=getxy(data2,sys.argv[2]+'['+sys.argv[3]+']')
    pl.subplot(2,2,3)
    pl.plot(x1,x1-x2,'bo')
    pl.xlabel('x1')
    pl.ylabel('x1-x2')
    pl.subplot(2,2,4)
    pl.plot(y1,y1-y2,'bo')
    pl.xlabel('y1')
    pl.ylabel('y1-y2')
    pl.show()
