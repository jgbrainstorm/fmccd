#!/usr/bin/env python2.6
"""
This code calculate xtalk coefficient table based on the data taken from xtalk_measurement.py

"""

from fermiMCCD import *

class ccd:
    def __init__(self, ext, bkp,da, pos):
        self.ext=ext
        self.bkp=bkp
        self.da=da
        self.pos=pos
        self.data=0
    def loaddata(self,imgNumber):
        if self.bkp == 3:
            imgName=gl.glob('/data_pan2/xtalk_auto_1_28_10/bkp3/*.fits')
            imgName.sort()
        if self.bkp == 1:
            imgName=gl.glob('/data_pan1/xtalk_auto_1_28_10/bkp1/*.fits')
            imgName.sort()
        if self.bkp == 4:
            imgName=gl.glob('/data_pan1/xtalk_auto_1_28_10/bkp4/*.fits')
            imgName.sort()
        self.data=pf.getdata(imgName[imgNumber],self.ext)    
        return('data loaded')


    
#----bkp4------

# For north, left and right are opposite.

n4l=ccd(1,4,9,'4N_L')
n4r=ccd(2,4,9,'4N_R')
n5l=ccd(3,4,9,'5N_L')
n5r=ccd(4,4,9,'5N_R')
n6l=ccd(5,4,9,'6N_L')
n6r=ccd(6,4,9,'6N_R')
n7l=ccd(7,4,9,'7N_L')
n7r=ccd(8,4,9,'7N_R')

s4l=ccd(13,4,8,'4S_L')
s4r=ccd(14,4,8,'4S_R')
s5l=ccd(15,4,8,'5S_L')
s5r=ccd(16,4,8,'5S_R')
s6l=ccd(17,4,8,'6S_L')
s6r=ccd(18,4,8,'6S_R')
s7l=ccd(19,4,8,'7S_L')
s7r=ccd(20,4,8,'7S_R')



#----bkp1--------
s2l=ccd(3,1,1,'2S_L')
s2r=ccd(4,1,1,'2S_R')
s3l=ccd(5,1,1,'3S_L')
s3r=ccd(6,1,1,'3S_R')


#----bkp3-----
s10l=ccd(1,3,5,'10S_L')
s10r=ccd(2,3,5,'10S_R')
s11l=ccd(3,3,5,'11S_L')
s11r=ccd(4,3,5,'11S_R')
s12l=ccd(5,3,5,'12S_L')
s12r=ccd(6,3,5,'12S_R')
s13l=ccd(7,3,5,'13S_L')
s13r=ccd(8,3,5,'13S_R')
s18l=ccd(9,3,5,'18S_L')
s18r=ccd(10,3,5,'18S_R')
s19l=ccd(11,3,5,'19S_L')
s19r=ccd(12,3,5,'19S_R')

s16l=ccd(13,3,6,'16S_L')
s16r=ccd(14,3,6,'16S_R')
s17l=ccd(15,3,6,'17S_L')
s17r=ccd(16,3,6,'17S_R')
s21l=ccd(17,3,6,'21S_L')
s21r=ccd(18,3,6,'21S_R')
s22l=ccd(19,3,6,'22S_L')
s22r=ccd(20,3,6,'22S_R')
s23l=ccd(21,3,6,'23S_L')
s23r=ccd(22,3,6,'23S_R')
s24l=ccd(23,3,6,'24S_L')
s24r=ccd(24,3,6,'24S_R')

s26l=ccd(25,3,7,'26S_L')
s26r=ccd(26,3,7,'26S_R')
s27l=ccd(27,3,7,'27S_L')
s27r=ccd(28,3,7,'27S_R')
s28l=ccd(29,3,7,'28S_L')
s28r=ccd(30,3,7,'28S_R')
s29l=ccd(31,3,7,'29S_L')
s29r=ccd(32,3,7,'29S_R')
s30l=ccd(33,3,7,'30S_L')
s30r=ccd(34,3,7,'30S_R')
s31l=ccd(35,3,7,'31S_L')
s31r=ccd(36,3,7,'31S_R')

CCD=[n4l,n4r,n5l,n5r,n6l,n6r,n7l,n7r,s7l,s7r,s6l,s6r,s5l,s5r,s4l,s4r,s3l,s3r,s2l,s2r,s10l,s10r,s11l,s11r,s12l,s12r,s13l,s13r,s19l,s19r,s18l,s18r,s17l,s17r,s16l,s16r,s21l,s21r,s22l,s22r,s23l,s23r,s24l,s24r,s28l,s28r,s27l,s27r,s26l,s26r,s29l,s29r,s30l,s30r,s31l,s31r]

N=len(CCD)
coef=np.zeros((N,N))

winSg=[200,900,1500,2700]
winBg=[200,900,300,800]

for i in range(N):
    for j in range(N):
        print i,'-----',j
        if j != i:
            coef[i,j]=xcoeff(i,CCD[i],CCD[j],winSg,winBg,'/data_pan2/xtalk_1_28_10_png/xtalk_auto_1_28_10_')         
        else:
            coef[i,j]=1.0
        CCD[i].data = 0
        CCD[j].data = 0
        
hdu=pf.PrimaryHDU(coef)
hdulist = pf.HDUList([hdu])
hdulist.writeto('/data_pan2/xtalk_1_28_10_png/xtalk_auto_1_28_10_coef.fits')

ccdName=('n4l','n4r','n5l','n5r','n6l','n6r','n7l','n7r','s7l','s7r','s6l','s6r','s5l','s5r','s4l','s4r','s3l','s3r','s2l','s2r','s10l','s10r','s11l','s11r','s12l','s12r','s13l','s13r','s19l','s19r','s18l','s18r','s17l','s17r','s16l','s16r','s21l','s21r','s22l','s22r','s23l','s23r','s24l','s24r','s28l','s28r','s27l','s27r','s26l','s26r','s29l','s29r','s30l','s30r','s31l','s31r')
N=len(ccdName)
coef=pf.getdata('/data_pan2/xtalk_1_28_10_png/xtalk_auto_1_28_10_coef.fits')
coef[(coef > 0.001)*(coef < 1)] = 3
coef[coef < -0.001] = 2
pl.figure(figsize=(45, 45)) 
pl.pcolor(coef,edgecolors='w',linewidths=0.1)
pl.colorbar()
pl.xticks(np.arange(N-1)+0.5,ccdName)
pl.yticks(np.arange(N-1)+0.5,ccdName)

ax=pl.axes()
ax.grid(color='r', linestyle='-', linewidth=2)



pl.savefig('/data_pan2/xtalk_1_28_10_png/xcoeff_matrix.png')

