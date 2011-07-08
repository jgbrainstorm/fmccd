from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

baseDir = '/home/jghao/research/ccd/imager/flatness_6_11_2011/rightside/'
cat=gl.glob(baseDir+'Image*catalog.fits')
cat.sort()
x=[0]
y=[0]
z=[0]
zerr=[0.01]
name=['n4']


l0,lerr0=offset(CCD1='n4',CCD2='n10',cat=cat,xadd=-60,yadd=0,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n10',CCD2='n4',cat=cat,xadd=60,yadd=0,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n10','n4')[0])
y.append(ccd_offset('n10','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n10')


l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=40,yadd=10,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=-40,yadd=-10,sep=70,crit_f=0)

zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n4')[0])
y.append(ccd_offset('s4','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s4')


l0,lerr0=offset(CCD1='n4',CCD2='s10',cat=cat,xadd=80,yadd=40,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s10',CCD2='n4',cat=cat,xadd=-80,yadd=-40,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s10','n4')[0])
y.append(ccd_offset('s10','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s10')


l0,lerr0=offset(CCD1='n4',CCD2='s9',cat=cat,xadd=80,yadd=60,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s9',CCD2='n4',cat=cat,xadd=-80,yadd=-60,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s9','n4')[0])
y.append(ccd_offset('s9','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s9')

l0,lerr0=offset(CCD1='n4',CCD2='s3',cat=cat,xadd=30,yadd=60,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s3',CCD2='n4',cat=cat,xadd=-30,yadd=-60,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s3','n4')[0])
y.append(ccd_offset('s3','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s3')

l0,lerr0=offset(CCD1='n4',CCD2='n3',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n3',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n3','n4')[0])
y.append(ccd_offset('n3','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n3')


l0,lerr0=offset(CCD1='n4',CCD2='n9',cat=cat,xadd=-50,yadd=60,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n9',CCD2='n4',cat=cat,xadd=50,yadd=-60,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n9','n4')[0])
y.append(ccd_offset('n9','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n9')


l0,lerr0=offset(CCD1='n4',CCD2='n2',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n2',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n2','n4')[0])
y.append(ccd_offset('n2','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n2')

l0,lerr0=offset(CCD1='n4',CCD2='s2',cat=cat,xadd=30,yadd=80,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s2',CCD2='n4',cat=cat,xadd=-30,yadd=-80,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s2','n4')[0])
y.append(ccd_offset('s2','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s2')

l0,lerr0=offset(CCD1='n4',CCD2='s8',cat=cat,xadd=80,yadd=90,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s8',CCD2='n4',cat=cat,xadd=-80,yadd=-90,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s8','n4')[0])
y.append(ccd_offset('s8','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s8')

l0,lerr0=offset(CCD1='n4',CCD2='s1',cat=cat,xadd=30,yadd=120,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='s1',CCD2='n4',cat=cat,xadd=-30,yadd=-120,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s1','n4')[0])
y.append(ccd_offset('s1','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s1')

l0,lerr0=offset(CCD1='n4',CCD2='n1',cat=cat,xadd=-10,yadd=100,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n1',CCD2='n4',cat=cat,xadd=10,yadd=-100,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n1','n4')[0])
y.append(ccd_offset('n1','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n1')


l0,lerr0=offset(CCD1='n4',CCD2='n8',cat=cat,xadd=-50,yadd=100,sep=70,crit_f=0)
l1,lerr1=offset(CCD1='n8',CCD2='n4',cat=cat,xadd=50,yadd=-100,sep=70,crit_f=0)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n8','n4')[0])
y.append(ccd_offset('n8','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n8')



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
from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

x=pf.getdata('flatness.fit').field('x')
y=pf.getdata('flatness.fit').field('y')
z=pf.getdata('flatness.fit').field('z')
zerr=pf.getdata('flatness.fit').field('zerr')
zoffset=pf.getdata('flatness.fit').field('zoffset')
name=pf.getdata('flatness.fit').field('CCD')


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
