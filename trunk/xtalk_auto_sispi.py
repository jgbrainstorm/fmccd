#!/usr/bin/env python
from fermiMCCD import *

class ccd:
    def __init__(self,ext):
        self.ext=ext
        self.pos=''
        self.left=0
    def loaddata(self,imgNumber,left):
        imgName=gl.glob('/data.02/xtalk_8_18_10/subtract/*.fits')
        imgName.sort()
        data=pf.getdata(imgName[imgNumber],self.ext)
        if left == 1:
            self.data=data[:,0:data.shape[1]/2]
        else:
            self.data=data[:,data.shape[1]/2:data.shape[1]]
        self.pos=pf.open(NameFits[imgNumber])[self.ext].header['DETSER']    
        return('data loaded')




#----bias subtraction--------
dir='/data.02/xtalk_8_18_10/'
NameFits=gl.glob(dir+'*.fits')
NameFits.sort()
NameBias=dir+'bias/Image_dark_002136.fits'
num=len(NameFits)
for i in range(num):
    print i
    subName=NameFits[i][:-5]+'_bias_sub.fits'
    t=Img_sub(NameFits[i],NameBias,subName)



#-----xtalk coefficients -------
dir='/data.02/xtalk_8_18_10/subtract/'
NameFits=gl.glob(dir+'*sub.fits')
ccd=['s1','s2','s3','s4','s5','s6','s9','s10','s11','s12','n6','n5','n4','n2','n1']
ext=[1,2,3,4,5,6,7,8,9,10,11,12,27,28,29,30,31,34]
for i in ext:
    
    
