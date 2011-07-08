#! /usr/bin/env python

from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *



ccd=['s22','s23','s24','s19','s18','s17','s11','s12','s13','s7','s6','s5','s4','n4','n5','n6','n7','n13','n12','n11','n17','n18','n19','n24','n23','n22']
fileNo=range(len(ccd))
ccd2fileNo=dict(zip(ccd,fileNo))



baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/leftside/'
cat=gl.glob(baseDir+'Image*catalog.fits')
cat.sort()

x=[]
y=[]
z=[]
zerr=[]
name=[]


#---row 1--------
l0,lerr0=offset(CCD1='n4',CCD2='n17',cat=cat,xadd=-150,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n17',CCD2='n4',cat=cat,xadd=100,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n17','n4')[0])
y.append(ccd_offset('n17','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n17')

l0,lerr0=offset(CCD1='n4',CCD2='n18',cat=cat,xadd=-100,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n18',CCD2='n4',cat=cat,xadd=100,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n18','n4')[0])
y.append(ccd_offset('n18','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n18')

l0,lerr0=offset(CCD1='n4',CCD2='n19',cat=cat,xadd=-100,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n19',CCD2='n4',cat=cat,xadd=100,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n19','n4')[0])
y.append(ccd_offset('n19','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n19')

#----row 2 -----

l0,lerr0=offset(CCD1='n4',CCD2='n11',cat=cat,xadd=-50,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n11',CCD2='n4',cat=cat,xadd=50,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n11','n4')[0])
y.append(ccd_offset('n11','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n11')

l0,lerr0=offset(CCD1='n4',CCD2='n12',cat=cat,xadd=-50,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n12',CCD2='n4',cat=cat,xadd=50,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n12','n4')[0])
y.append(ccd_offset('n12','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n12')

l0,lerr0=offset(CCD1='n4',CCD2='n13',cat=cat,xadd=-50,yadd=-70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n13',CCD2='n4',cat=cat,xadd=50,yadd=70,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n13','n4')[0])
y.append(ccd_offset('n13','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n13')


#----row 3-----

x.append(0)
y.append(0)
z.append(0)
zerr.append(0)
name.append('n4')


l0,lerr0=offset(CCD1='n4',CCD2='n5',cat=cat,xadd=0,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n5','n4')[0])
y.append(ccd_offset('n5','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n5')

l0,lerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n6','n4')[0])
y.append(ccd_offset('n6','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')

l0,lerr0=offset(CCD1='n4',CCD2='n7',cat=cat,xadd=20,yadd=-90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n7',CCD2='n4',cat=cat,xadd=-20,yadd=90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n7','n4')[0])
y.append(ccd_offset('n7','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n7')


#----row 4 -----
l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=40,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=-40,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n4')[0])
y.append(ccd_offset('s4','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s4')

l0,lerr0=offset(CCD1='n4',CCD2='s5',cat=cat,xadd=60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s5',CCD2='n4',cat=cat,xadd=-60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s5','n4')[0])
y.append(ccd_offset('s5','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s5')

l0,lerr0=offset(CCD1='n4',CCD2='s6',cat=cat,xadd=60,yadd=-10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s6',CCD2='n4',cat=cat,xadd=-60,yadd=10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s6','n4')[0])
y.append(ccd_offset('s6','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s6')


l0,lerr0=offset(CCD1='n4',CCD2='s7',cat=cat,xadd=60,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s7',CCD2='n4',cat=cat,xadd=-60,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s7','n4')[0])
y.append(ccd_offset('s7','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s7')


#---row 5 ----

l0,lerr0=offset(CCD1='n4',CCD2='s11',cat=cat,xadd=100,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s11',CCD2='n4',cat=cat,xadd=-100,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s11','n4')[0])
y.append(ccd_offset('s11','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s11')

l0,lerr0=offset(CCD1='n4',CCD2='s12',cat=cat,xadd=100,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s12',CCD2='n4',cat=cat,xadd=-100,yadd=-0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s12','n4')[0])
y.append(ccd_offset('s12','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s12')

l0,lerr0=offset(CCD1='n4',CCD2='s13',cat=cat,xadd=100,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s13',CCD2='n4',cat=cat,xadd=-100,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s13','n4')[0])
y.append(ccd_offset('s13','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s13')


#---row 6 ----

l0,lerr0=offset(CCD1='n4',CCD2='s17',cat=cat,xadd=150,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s17',CCD2='n4',cat=cat,xadd=-150,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s17','n4')[0])
y.append(ccd_offset('s17','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s17')


l0,lerr0=offset(CCD1='n4',CCD2='s18',cat=cat,xadd=150,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s18',CCD2='n4',cat=cat,xadd=-150,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s18','n4')[0])
y.append(ccd_offset('s18','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s18')

l0,lerr0=offset(CCD1='n4',CCD2='s19',cat=cat,xadd=150,yadd=-30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s19',CCD2='n4',cat=cat,xadd=-150,yadd=30,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s19','n4')[0])
y.append(ccd_offset('s19','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s19')


#---row 7-----

l0,lerr0=offset(CCD1='n4',CCD2='s22',cat=cat,xadd=190,yadd=50,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s22',CCD2='n4',cat=cat,xadd=-190,yadd=-50,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s22','n4')[0])
y.append(ccd_offset('s22','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s22')

l0,lerr0=offset(CCD1='n4',CCD2='s24',cat=cat,xadd=200,yadd=-20,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s24',CCD2='n4',cat=cat,xadd=-200,yadd=20,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s24','n4')[0])
y.append(ccd_offset('s24','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s24')




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

p=np.array([0.001586,-0.002875,1.331791]) #from lm fit in R
zoffset=z-plane(p,x,y)

c1=pf.Column(name='x',format='D',array=x)
c2=pf.Column(name='y',format='D',array=y)
c3=pf.Column(name='z',format='D',array=z)
c4=pf.Column(name='zerr',format='D',array=zerr)
c5=pf.Column(name='zoffset',format='D',array=zoffset)
c6=pf.Column(name='CCD',format='10A',array=name)

hdu=pf.new_table([c1,c2,c3,c4,c5,c6])
hdu.writeto(baseDir+'flatness_left.fit')

data=zip(x,y,z)
data=np.array(data)
np.savetxt(baseDir+'flatness_left.txt',data)

"""
----analysis----

#start ipython -wthread

from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

baseDir = '/home/jghao/research/ccd/imager/flatness_6_24_11/leftside/'

x=pf.getdata(baseDir+'flatness_left.fit').field('x')
y=pf.getdata(baseDir+'flatness_left.fit').field('y')
z=pf.getdata(baseDir+'flatness_left.fit').field('z')
zerr=pf.getdata(baseDir+'flatness_left.fit').field('zerr')
zoffset=pf.getdata(baseDir+'flatness_left.fit').field('zoffset')
name=pf.getdata(baseDir+'flatness_left.fit').field('CCD')

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
zz=z/5.
zzoffset=zoffset/5.

barchart(xx,yy,zz)
barchart(xx,yy,zzoffset)

"""
