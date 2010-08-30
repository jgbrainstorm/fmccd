#!/usr/bin/env python2.6
"""
This code calculate xtalk coefficient table based on the data taken from xtalk_measurement.py. It is updated from the 

"""

from fermiMCCD import *

class ccd:
    def __init__(self, ext,pos):
        self.ext=ext
        self.pos=pos
        self.data=0
    def loaddata(self,imgNumber):
        imgName=gl.glob('/data.02/xtalk_8_21_10/full/*sub*.fits')
        imgName.sort()
        self.data=pf.getdata(imgName[imgNumber],self.ext)    
        return('data loaded')

"""
#--------get bias subtracted-----------------
dir='/data.02/xtalk_8_21_10/full/'
NameFits=gl.glob(dir+'*.fits')
NameFits.sort()
NameBias=dir+'bias/bias.fits'
num=len(NameFits)
for i in range(num):
    print i
    subName=NameFits[i][:-5]+'_bias_sub.fits'
    t=Img_sub(NameFits[i],NameBias,subName)
"""
#----------data taking sequnce---------------------
#ccd=['s1','s2','s3','s4','s5','s6','s7','n7','n6','n5','n4','n2','n1','s9','s10','s11','s12','s13']


#----bkp1--------
s1l=ccd(53,'1S_L')
s1r=ccd(54,'1S_R')
s2l=ccd(55,'2S_L')
s2r=ccd(56,'2S_R')
s3l=ccd(57,'3S_L')
s3r=ccd(58,'3S_R')
s9l=ccd(67,'9S_L')
s9r=ccd(68,'9S_R')
n1l=ccd(59,'1N_L')
n1r=ccd(60,'1N_R')
n2l=ccd(61,'2N_L')
n2r=ccd(62,'2N_R')

#------bkp3---------

s10l=ccd(17,'10S_L')
s10r=ccd(18,'10S_R')
s11l=ccd(19,'11S_L')
s11r=ccd(20,'11S_R')
s12l=ccd(21,'12S_L')
s12r=ccd(22,'12S_R')
s13l=ccd(23,'13S_L')
s13r=ccd(24,'13S_R')


  
#----bkp4------

# For north, left and right are opposite.

n4l=ccd(1,'4N_L')
n4r=ccd(2,'4N_R')
n5l=ccd(3,'5N_L')
n5r=ccd(4,'5N_R')
n6l=ccd(5,'6N_L')
n6r=ccd(6,'6N_R')
n7l=ccd(7,'7N_L')
n7r=ccd(8,'7N_R')

s4l=ccd(9,'4S_L')
s4r=ccd(10,'4S_R')
s5l=ccd(11,'5S_L')
s5r=ccd(12,'5S_R')
s6l=ccd(13,'6S_L')
s6r=ccd(14,'6S_R')
s7l=ccd(15,'7S_L')
s7r=ccd(26,'7S_R')






CCD=[s1l,s1r,s2l,s2r,s3l,s3r,s4l,s4r,s5l,s5r,s6l,s6r,s7l,s7r,n7l,n7r,n6l,n6r,n5l,n5r,n4l,n4r,n2l,n2r,n1l,n1r,s9l,s9r,s10l,s10r,s11l,s11r,s12l,s12r,s13l,s13r]

N=len(CCD)
coef=np.zeros((N,N))

winSg=[1600,2300,300,900]
winBg=[3700,3900,300,600]
dir='/data.02/xtalk_8_21_10/full/'
for i in range(N):
    for j in range(N):
        print i,'-----',j
        if j != i:
            NamePng=dir+'fig/8_21_10_'
            coef[i,j]=xcoeff(i,CCD[i],CCD[j],winSg,winBg,NamePng)         
        else:
            coef[i,j]=1.0
        CCD[i].data = 0
        CCD[j].data = 0
        
hdu=pf.PrimaryHDU(coef)
hdulist = pf.HDUList([hdu])
hdulist.writeto(dir+'xtalk_auto_8_21_10_coef.fits')



#---------analysis of data----------

dir='/data.02/xtalk_8_21_10/full/'

ccdName=['s1l','s1r','s2l','s2r','s3l','s3r','s4l','s4r','s5l','s5r','s6l','s6r','s7l','s7r','n7l','n7r','n6l','n6r','n5l','n5r','n4l','n4r','n2l','n2r','n1l','n1r','s9l','s9r','s10l','s10r','s11l','s11r','s12l','s12r','s13l','s13r']


N=len(ccdName)
coef=pf.getdata(dir+'xtalk_auto_8_21_10_coef.fits')
coef[(coef > 0.001)*(coef < 1)] = 3
coef[coef < -0.001] = 2
pl.figure(figsize=(45, 45)) 
pl.pcolor(coef,edgecolors='w',linewidths=0.1)
pl.colorbar()
pl.xticks(np.arange(N-1)+0.5,ccdName)
pl.yticks(np.arange(N-1)+0.5,ccdName)

ax=pl.axes()
ax.grid(color='r', linestyle='-', linewidth=2)

pl.savefig(dir+'fig/spec_xcoeff_matrix.png')
pl.close()


coef=pf.getdata(dir+'xtalk_auto_8_21_10_coef.fits')
coef[(coef > 0.0001)*(coef < 1)] = 3
coef[coef < -0.0001] = 2
pl.figure(figsize=(45, 45)) 
pl.pcolor(coef,edgecolors='w',linewidths=0.1)
pl.colorbar()
pl.xticks(np.arange(N-1)+0.5,ccdName)
pl.yticks(np.arange(N-1)+0.5,ccdName)

ax=pl.axes()
ax.grid(color='r', linestyle='-', linewidth=2)

pl.savefig(dir+'fig/0.0001_xcoeff_matrix.png')
pl.close()


coef=pf.getdata(dir+'xtalk_auto_8_21_10_coef.fits')
coef[(coef > 0.0002)*(coef < 1)] = 3
coef[coef < -0.0002] = 2
pl.figure(figsize=(45, 45)) 
pl.pcolor(coef,edgecolors='w',linewidths=0.1)
pl.colorbar()
pl.xticks(np.arange(N-1)+0.5,ccdName)
pl.yticks(np.arange(N-1)+0.5,ccdName)

ax=pl.axes()
ax.grid(color='r', linestyle='-', linewidth=2)

pl.savefig(dir+'fig/0.0002_xcoeff_matrix.png')
pl.close()


coef=pf.getdata(dir+'xtalk_auto_8_21_10_coef.fits')
coef[(coef > 0.0005)*(coef < 1)] = 3
coef[coef < -0.0005] = 2
pl.figure(figsize=(45, 45)) 
pl.pcolor(coef,edgecolors='w',linewidths=0.1)
pl.colorbar()
pl.xticks(np.arange(N-1)+0.5,ccdName)
pl.yticks(np.arange(N-1)+0.5,ccdName)

ax=pl.axes()
ax.grid(color='r', linestyle='-', linewidth=2)

pl.savefig(dir+'fig/0.0005_xcoeff_matrix.png')
pl.close()
