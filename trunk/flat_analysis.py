from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *


baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/rightside/'

xr=pf.getdata(baseDir+'flatness_right.fit').field('x')
yr=pf.getdata(baseDir+'flatness_right.fit').field('y')
zr=pf.getdata(baseDir+'flatness_right.fit').field('z')
zerrr=pf.getdata(baseDir+'flatness_right.fit').field('zerr')
zoffsetr=pf.getdata(baseDir+'flatness_right.fit').field('zoffset')
namer=pf.getdata(baseDir+'flatness_right.fit').field('CCD')


baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/leftside/'

xl=pf.getdata(baseDir+'flatness_left.fit').field('x')
yl=pf.getdata(baseDir+'flatness_left.fit').field('y')
zl=pf.getdata(baseDir+'flatness_left.fit').field('z')
zerrl=pf.getdata(baseDir+'flatness_left.fit').field('zerr')
zoffsetl=pf.getdata(baseDir+'flatness_left.fit').field('zoffset')
namel=pf.getdata(baseDir+'flatness_left.fit').field('CCD')


def plotrowL(idx):
    pl.plot(np.arange(len(namel[idx])),z[idx],'b.')
    pl.errorbar(np.arange(len(namel[idx])),zl[idx],yerr=zerrl[idx],ecolor='b',fmt='.')
    pl.xticks(np.arange(len(namel[idx])),namel[idx])
    pl.hlines(np.median(zl[idx]),-1,len(xl[idx])+1,'r')
    pl.hlines(np.median(zl[idx])+2.1,-1,len(xl[idx])+1,'g')
    pl.hlines(np.median(zl[idx])-2.1,-1,len(xl[idx])+1,'g')
    pl.ylabel('offset (pixels)')
    pl.xlabel('CCDs')

def plotrowR(idx):
    pl.plot(np.arange(len(namer[idx])),zoffsetr[idx],'b.')
    pl.errorbar(np.arange(len(namer[idx])),zoffsetr[idx],yerr=zerrr[idx],ecolor='b',fmt='.')
    pl.xticks(np.arange(len(namer[idx])),namer[idx])
    pl.hlines(np.median(zoffsetr[idx]),-1,len(xr[idx])+1,'r')
    pl.hlines(np.median(zoffsetr[idx])+2.1,-1,len(xr[idx])+1,'g')
    pl.hlines(np.median(zoffsetr[idx])-2.1,-1,len(xr[idx])+1,'g')
    pl.ylabel('offset (pixels)')
    pl.xlabel('CCDs')


scale=2048.
xx=x/scale
yy=y/scale
zz=z/20.
zzoffset=zoffset/20.

barchart(xx,yy,zz)
barchart(xx,yy,zzoffset)

