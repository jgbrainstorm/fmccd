from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

baseDir = '/home/jghao/research/ccd/flatness/flatness_5_20_10/flatness_5_20_10_data/'
cat=gl.glob(baseDir+'Image_hao_*catalog.fits')
cat.sort()

x=[0]
y=[0]
z=[0]
zerr=[0.01]
name=['n4']

l0,lerr0=offset(CCD1='n4',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n5')[0])
y.append(ccd_offset('n4','n5')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n5')

l0,lerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=150,sep=70,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n6')[0])
y.append(ccd_offset('n4','n6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')


l0,lerr0=offset(CCD1='n4',CCD2='n7',cat=cat,xadd=30,yadd=-170,sep=70,crit_f=80)
l1,lerr1=offset(CCD1='n7',CCD2='n4',cat=cat,xadd=-30,yadd=170,sep=70,crit_f=80)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','n7')[0])
y.append(ccd_offset('n4','n7')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n7')


l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s4')[0])
y.append(ccd_offset('n4','s4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s4')

l0,lerr0=offset(CCD1='n4',CCD2='s5',cat=cat,xadd=0,yadd=0,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=80,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s5')[0])
y.append(ccd_offset('n4','s5')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s5')

l0,lerr0=offset(CCD1='n4',CCD2='s6',cat=cat,xadd=80,yadd=-100,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s6',CCD2='n4',cat=cat,xadd=-80,yadd=100,sep=80,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s6')[0])
y.append(ccd_offset('n4','s6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s6')

l0,lerr0=offset(CCD1='n4',CCD2='s7',cat=cat,xadd=100,yadd=-150,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s7',CCD2='n4',cat=cat,xadd=-100,yadd=150,sep=80,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s7')[0])
y.append(ccd_offset('n4','s7')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s7')

l0,lerr0=offset(CCD1='n4',CCD2='s10',cat=cat,xadd=100,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s10',CCD2='n4',cat=cat,xadd=-100,yadd=0,sep=70,crit_f=8)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s10')[0])
y.append(ccd_offset('n4','s10')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s10')

l0,lerr0=offset(CCD1='n4',CCD2='s11',cat=cat,xadd=100,yadd=0,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s11',CCD2='n4',cat=cat,xadd=-100,yadd=-0,sep=70,crit_f=20)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s11')[0])
y.append(ccd_offset('n4','s11')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s11')


l0,lerr0=offset(CCD1='n4',CCD2='s12',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=8)
l1,lerr1=offset(CCD1='s12',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=8)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s12')[0])
y.append(ccd_offset('n4','s12')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s12')


l0,lerr0=offset(CCD1='n4',CCD2='s13',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s13',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s13')[0])
y.append(ccd_offset('n4','s13')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s13')

l0,lerr0=offset(CCD1='n4',CCD2='s16',cat=cat,xadd=130,yadd=-30,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s16',CCD2='n4',cat=cat,xadd=-130,yadd=30,sep=70,crit_f=20)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s16')[0])
y.append(ccd_offset('n4','s16')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s16')

l0,lerr0=offset(CCD1='n4',CCD2='s17',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s17',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s17')[0])
y.append(ccd_offset('n4','s17')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s17')

l0,lerr0=offset(CCD1='n4',CCD2='s18',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s18',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s18')[0])
y.append(ccd_offset('n4','s18')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s18')

l0,lerr0=offset(CCD1='n4',CCD2='s19',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s19',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s19')[0])
y.append(ccd_offset('n4','s19')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s19')

l0,lerr0=offset(CCD1='n4',CCD2='s21',cat=cat,xadd=100,yadd=-1200,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s21',CCD2='n4',cat=cat,xadd=-100,yadd=1200,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s21')[0])
y.append(ccd_offset('n4','s21')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s21')

l0,lerr0=offset(CCD1='n4',CCD2='s22',cat=cat,xadd=100,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s22',CCD2='n4',cat=cat,xadd=-100,yadd=0,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s22')[0])
y.append(ccd_offset('n4','s22')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s22')

l0,lerr0=offset(CCD1='n4',CCD2='s23',cat=cat,xadd=150,yadd=-50,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s23',CCD2='n4',cat=cat,xadd=-150,yadd=50,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s23')[0])
y.append(ccd_offset('n4','s23')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s23')

l0,lerr0=offset(CCD1='n4',CCD2='s24',cat=cat,xadd=200,yadd=-150,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s24',CCD2='n4',cat=cat,xadd=-200,yadd=150,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s24')[0])
y.append(ccd_offset('n4','s24')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s24')

l0,lerr0=offset(CCD1='n4',CCD2='s26',cat=cat,xadd=200,yadd=-50,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s26',CCD2='n4',cat=cat,xadd=-200,yadd=50,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s26')[0])
y.append(ccd_offset('n4','s26')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s26')

l0,lerr0=offset(CCD1='n4',CCD2='s27',cat=cat,xadd=200,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s27',CCD2='n4',cat=cat,xadd=-200,yadd=0,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s27')[0])
y.append(ccd_offset('n4','s27')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s27')

l0,lerr0=offset(CCD1='n4',CCD2='s28',cat=cat,xadd=200,yadd=-50,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='s28',CCD2='n4',cat=cat,xadd=-200,yadd=50,sep=70,crit_f=30)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s28')[0])
y.append(ccd_offset('n4','s28')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s28')

l0,lerr0=offset(CCD1='n4',CCD2='s29',cat=cat,xadd=200,yadd=-1250,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s29',CCD2='n4',cat=cat,xadd=-200,yadd=1250,sep=70,crit_f=20)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s29')[0])
y.append(ccd_offset('n4','s29')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s29')

l0,lerr0=offset(CCD1='n4',CCD2='s30',cat=cat,xadd=200,yadd=0,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s30',CCD2='n4',cat=cat,xadd=-200,yadd=0,sep=70,crit_f=20)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s30')[0])
y.append(ccd_offset('n4','s30')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s30')

l0,lerr0=offset(CCD1='n4',CCD2='s31',cat=cat,xadd=250,yadd=-270,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s31',CCD2='n4',cat=cat,xadd=-250,yadd=270,sep=70,crit_f=10)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('n4','s31')[0])
y.append(ccd_offset('n4','s31')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s31')

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
