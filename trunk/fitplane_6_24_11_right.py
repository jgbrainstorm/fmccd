#! /usr/bin/env python
from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
r=robjects.r

ccd=['s22','s21','s20','s14','s15','s16','s10','s9','s8','s1','s2','s3','s4','n4','n3','n2','n1','n8','n9','n10','n16','n15','n14','n20','n21','n22']

fileNo=range(len(ccd))
ccd2fileNo=dict(zip(ccd,fileNo))



baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/rightside/'
cat=gl.glob(baseDir+'Image*catalog.fits')
cat.sort()
x=[]
y=[]
z=[]
zerr=[]
name=[]


"""
l0,lerr0=offset(CCD1='n4',CCD2='n22',cat=cat,xadd=220,yadd=20,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n22',CCD2='n4',cat=cat,xadd=-220,yadd=-20,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n22','n4')[0])
y.append(ccd_offset('n22','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n22')

l0,lerr0=offset(CCD1='n4',CCD2='n21',cat=cat,xadd=220,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n21',CCD2='n4',cat=cat,xadd=-220,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n21','n4')[0])
y.append(ccd_offset('n21','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n21')

l0,lerr0=offset(CCD1='n4',CCD2='n20',cat=cat,xadd=220,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n20',CCD2='n4',cat=cat,xadd=-220,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n20','n4')[0])
y.append(ccd_offset('n20','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n20')

"""


#-------row 1---------
l0,lerr0=offset(CCD1='n4',CCD2='n14',cat=cat,xadd=-100,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n14',CCD2='n4',cat=cat,xadd=100,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n14','n4')[0])
y.append(ccd_offset('n14','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n14')

l0,lerr0=offset(CCD1='n4',CCD2='n15',cat=cat,xadd=-120,yadd=70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n15',CCD2='n4',cat=cat,xadd=120,yadd=-70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n15','n4')[0])
y.append(ccd_offset('n15','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n15')


#---row2-------


l0,lerr0=offset(CCD1='n4',CCD2='n8',cat=cat,xadd=-50,yadd=100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n8',CCD2='n4',cat=cat,xadd=50,yadd=-100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n8','n4')[0])
y.append(ccd_offset('n8','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n8')

l0,lerr0=offset(CCD1='n4',CCD2='n9',cat=cat,xadd=-50,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n9',CCD2='n4',cat=cat,xadd=50,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n9','n4')[0])
y.append(ccd_offset('n9','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n9')

l0,lerr0=offset(CCD1='n4',CCD2='n10',cat=cat,xadd=-60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n10',CCD2='n4',cat=cat,xadd=60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n10','n4')[0])
y.append(ccd_offset('n10','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n10')


#------row 3-------------

l0,lerr0=offset(CCD1='n4',CCD2='n1',cat=cat,xadd=-10,yadd=100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n1',CCD2='n4',cat=cat,xadd=10,yadd=-100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n1','n4')[0])
y.append(ccd_offset('n1','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n1')


l0,lerr0=offset(CCD1='n4',CCD2='n2',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n2',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n2','n4')[0])
y.append(ccd_offset('n2','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n2')

l0,lerr0=offset(CCD1='n4',CCD2='n3',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n3',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n3','n4')[0])
y.append(ccd_offset('n3','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n3')

x.append(0)
y.append(0)
z.append(0)
zerr.append(0)
name.append('n4')




#-----row 4 -----
l0,lerr0=offset(CCD1='n4',CCD2='s1',cat=cat,xadd=30,yadd=120,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s1',CCD2='n4',cat=cat,xadd=-30,yadd=-120,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s1','n4')[0])
y.append(ccd_offset('s1','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s1')

l0,lerr0=offset(CCD1='n4',CCD2='s2',cat=cat,xadd=30,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s2',CCD2='n4',cat=cat,xadd=-30,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s2','n4')[0])
y.append(ccd_offset('s2','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s2')

l0,lerr0=offset(CCD1='n4',CCD2='s3',cat=cat,xadd=30,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s3',CCD2='n4',cat=cat,xadd=-30,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s3','n4')[0])
y.append(ccd_offset('s3','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s3')

l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=40,yadd=10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=-40,yadd=-10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n4')[0])
y.append(ccd_offset('s4','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s4')


#----row 5 -----

l0,lerr0=offset(CCD1='n4',CCD2='s8',cat=cat,xadd=80,yadd=90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s8',CCD2='n4',cat=cat,xadd=-80,yadd=-90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s8','n4')[0])
y.append(ccd_offset('s8','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s8')

l0,lerr0=offset(CCD1='n4',CCD2='s9',cat=cat,xadd=80,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s9',CCD2='n4',cat=cat,xadd=-80,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s9','n4')[0])
y.append(ccd_offset('s9','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s9')

l0,lerr0=offset(CCD1='n4',CCD2='s10',cat=cat,xadd=80,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s10',CCD2='n4',cat=cat,xadd=-80,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s10','n4')[0])
y.append(ccd_offset('s10','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s10')

#----row 6------

l0,lerr0=offset(CCD1='n4',CCD2='s14',cat=cat,xadd=150,yadd=110,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s14',CCD2='n4',cat=cat,xadd=-150,yadd=-110,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s14','n4')[0])
y.append(ccd_offset('s14','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s14')


l0,lerr0=offset(CCD1='n4',CCD2='s15',cat=cat,xadd=150,yadd=70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s15',CCD2='n4',cat=cat,xadd=-150,yadd=-70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s15','n4')[0])
y.append(ccd_offset('s15','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s15')


l0,lerr0=offset(CCD1='n4',CCD2='s16',cat=cat,xadd=130,yadd=70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s16',CCD2='n4',cat=cat,xadd=-130,yadd=-70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s16','n4')[0])
y.append(ccd_offset('s16','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s16')


#----row 7 ------

l0,lerr0=offset(CCD1='n4',CCD2='s20',cat=cat,xadd=180,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s20',CCD2='n4',cat=cat,xadd=-180,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s20','n4')[0])
y.append(ccd_offset('s20','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s20')

l0,lerr0=offset(CCD1='n4',CCD2='s21',cat=cat,xadd=180,yadd=110,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s21',CCD2='n4',cat=cat,xadd=-180,yadd=-110,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s21','n4')[0])
y.append(ccd_offset('s21','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s21')

l0,lerr0=offset(CCD1='n4',CCD2='s22',cat=cat,xadd=200,yadd=50,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s22',CCD2='n4',cat=cat,xadd=-200,yadd=-50,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s22','n4')[0])
y.append(ccd_offset('s22','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s22')

x=np.array(x)
y=np.array(y)
z=np.array(z)
zerr=np.array(zerr)

def bfplane(p,x,y,z,zerr):
    A=p[0]
    B=p[1]
    C=p[2]
    res=((A*x+B*y+C)-z)/zerr
    return res

def plane(p,x,y):
    A=p[0]
    B=p[1]
    C=p[2]
    res=(A*x+B*y+C)
    return res

p0=np.array([0.002,-0.002,2.37])
plsq=leastsq(bfplane,p0,args=(x,y,z,zerr),full_output=1) 

p=np.array([0.002341,-0.002709,2.373421])

zoffset=z-plane(p,x,y)

c1=pf.Column(name='x',format='D',array=x)
c2=pf.Column(name='y',format='D',array=y)
c3=pf.Column(name='z',format='D',array=z)
c4=pf.Column(name='zerr',format='D',array=zerr)
c5=pf.Column(name='zoffset',format='D',array=zoffset)
c6=pf.Column(name='CCD',format='10A',array=name)

hdu=pf.new_table([c1,c2,c3,c4,c5,c6])
hdu.writeto(baseDir+'flatness_right.fit')

data=zip(x,y,z)
data=np.array(data)
np.savetxt(baseDir+'flatness_right.txt',data)



"""
----analysis----
from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *


baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/rightside/'

x=pf.getdata(baseDir+'flatness_right.fit').field('x')
y=pf.getdata(baseDir+'flatness_right.fit').field('y')
z=pf.getdata(baseDir+'flatness_right.fit').field('z')
zerr=pf.getdata(baseDir+'flatness_right.fit').field('zerr')
zoffset=pf.getdata(baseDir+'flatness_right.fit').field('zoffset')
name=pf.getdata(baseDir+'flatness_right.fit').field('CCD')

pl.figure(figsize=(11,6))
pl.plot(np.arange(len(name)),zoffset,'b.')
pl.errorbar(np.arange(len(name)),zoffset,yerr=zerr,ecolor='b',fmt='.')
pl.xticks(np.arange(len(name)),name)
pl.hlines(np.median(zoffset),-1,len(x)+1,'r')
pl.hlines(np.median(zoffset)+2.1,-1,len(x)+1,'g')
pl.hlines(np.median(zoffset)-2.1,-1,len(x)+1,'g')
pl.ylabel('offset (pixels)')
pl.xlabel('CCDs')


scale=2048.
xx=x/scale
yy=y/scale
zz=z/20.
zzoffset=zoffset/20.

barchart(xx,yy,zz)
barchart(xx,yy,zzoffset)


"""
