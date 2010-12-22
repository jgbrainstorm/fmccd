from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

baseDir = '/home/jghao/research/ccd/imager/flatness_8_21_10/'
cat=gl.glob(baseDir+'Image*catalog.fits')
cat.sort()

x=[0]
y=[0]
z=[0]
zerr=[0.01]
name=['n4']

l0,lerr0=offset(CCD1='n4',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=5)
l1,lerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=5)

zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n5')[0])
y.append(ccd_offset('n4','n5')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n5')


l0,lerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=3)
l1,lerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=3)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n6')[0])
y.append(ccd_offset('n4','n6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')

l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=3)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=3)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s4')[0])
y.append(ccd_offset('n4','s4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')






l0,lerr0=offset(CCD1='n5',CCD2='n6',cat=cat,xadd=0,yadd=0,sep=70,crit_f=1)
l1,lerr1=offset(CCD1='n6',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=1)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n6')[0])
y.append(ccd_offset('n4','n6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')








l0,lerr0=offset(CCD1='n4',CCD2='n7',cat=cat,xadd=-150,yadd=150,sep=70,crit_f=3)
l1,lerr1=offset(CCD1='n7',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=3)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n7')[0])
y.append(ccd_offset('n4','n7')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n7')




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


p0=np.array([0.,0.,8.])
plsq=leastsq(bfplane,p0,args=(x,y,z,zerr),full_output=1) 

p=np.array(plsq[0])
zoffset=z-plane(p,x,y)

c1=pf.Column(name='x',format='D',array=x)
c2=pf.Column(name='y',format='D',array=y)
c3=pf.Column(name='z',format='D',array=z)
c4=pf.Column(name='zerr',format='D',array=zerr)
c5=pf.Column(name='zoffset',format='D',array=zoffset)
c6=pf.Column(name='CCD',format='10A',array=name)

hdu=pf.new_table([c1,c2,c3,c4,c5,c6])
hdu.writeto('flatness.fit')




"""
----analysis----

x=pf.getdata('flatness.fit').field('x')
y=pf.getdata('flatness.fit').field('y')
z=pf.getdata('flatness.fit').field('z')
zerr=pf.getdata('flatness.fit').field('zerr')
zoffset=pf.getdata('flatness.fit').field('zoffset')
name=pf.getdata('flatness.fit').field('CCD')


pl.plot(np.arange(len(name)),zoffset,'b.')
pl.errorbar(np.arange(len(name)),zoffset,yerr=zerr,ecolor='b',fmt='.')
pl.xticks(np.arange(len(name)),name)
pl.hlines(np.median(zoffset),-1,27,'r')
pl.hlines(np.median(zoffset)+2.1,-1,27,'g')
pl.hlines(np.median(zoffset)-2.1,-1,27,'g')
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
