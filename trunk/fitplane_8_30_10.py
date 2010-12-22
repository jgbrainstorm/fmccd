from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

baseDir = '/home/jghao/research/ccd/imager/flatness_8_30_10/'
cat=gl.glob(baseDir+'Image*catalog.fits')
check=gl.glob(baseDir+'Image*check.fits')
cat.sort()
check.sort()

#------use s4 as reference. there is no n3, s7,n7,s1,n1
x=[0]
y=[0]
z=[0]
zerr=[0.01]
name=['s4']


#----s2------
l0,lerr0=offset(CCD1='s4',CCD2='s2',cat=cat,xadd=0,yadd=100,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s2.png')
pl.close()
l1,lerr1=offset(CCD1='s2',CCD2='s4',cat=cat,xadd=0,yadd=-100,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s2s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s2')[0])
y.append(ccd_offset('s4','s2')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s2')


#----s3-------
l0,lerr0=offset(CCD1='s4',CCD2='s3',cat=cat,xadd=0,yadd=50,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s3.png')
pl.close()
l1,lerr1=offset(CCD1='s3',CCD2='s4',cat=cat,xadd=0,yadd=-50,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s3s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s3')[0])
y.append(ccd_offset('s4','s3')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s3')


#----s5-------
l0,lerr0=offset(CCD1='s4',CCD2='s5',cat=cat,xadd=0,yadd=-50,sep=70,crit_f=5)
l1,lerr1=offset(CCD1='s5',CCD2='s4',cat=cat,xadd=0,yadd=50,sep=70,crit_f=5)
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s5')[0])
y.append(ccd_offset('s4','s5')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s5')


#----s6-------
l0,lerr0=offset(CCD1='s4',CCD2='s6',cat=cat,xadd=0,yadd=-100,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s6.png')
pl.close()
l1,lerr1=offset(CCD1='s6',CCD2='s4',cat=cat,xadd=0,yadd=100,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s6s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s6')[0])
y.append(ccd_offset('s4','s6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s6')




#----n2-------
l0,lerr0=offset(CCD1='s4',CCD2='n2',cat=cat,xadd=-30,yadd=100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s4n2.png')
pl.close()
l1,lerr1=offset(CCD1='n2',CCD2='s4',cat=cat,xadd=30,yadd=-100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/n2s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n2')[0])
y.append(ccd_offset('s4','n2')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n2')


#----n4-------
l0,lerr0=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=-40,yadd=0,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s4n4.png')
pl.close()
l1,lerr1=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=40,yadd=0,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/n4s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n4')[0])
y.append(ccd_offset('s4','n4')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n4')

#----n5-------
l0,lerr0=offset(CCD1='s4',CCD2='n5',cat=cat,xadd=-50,yadd=-40,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4n5.png')
pl.close()
l1,lerr1=offset(CCD1='n5',CCD2='s4',cat=cat,xadd=50,yadd=40,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/n5s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n5')[0])
y.append(ccd_offset('s4','n5')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n5')


#----n6-------
l0,lerr0=offset(CCD1='s4',CCD2='n6',cat=cat,xadd=-50,yadd=-80,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s4n6.png')
pl.close()
l1,lerr1=offset(CCD1='n6',CCD2='s4',cat=cat,xadd=50,yadd=80,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/n6s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','n6')[0])
y.append(ccd_offset('s4','n6')[1])
z.append(zm)
zerr.append(zmerr)
name.append('n6')

#----s9-------
l0,lerr0=offset(CCD1='s4',CCD2='s9',cat=cat,xadd=40,yadd=80,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s9.png')
pl.close()
l1,lerr1=offset(CCD1='s9',CCD2='s4',cat=cat,xadd=-40,yadd=-80,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s9s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s9')[0])
y.append(ccd_offset('s4','s9')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s9')


#----s10-------
l0,lerr0=offset(CCD1='s4',CCD2='s10',cat=cat,xadd=40,yadd=40,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s10.png')
pl.close()
l1,lerr1=offset(CCD1='s10',CCD2='s4',cat=cat,xadd=-40,yadd=-40,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s10s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s10')[0])
y.append(ccd_offset('s4','s10')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s10')

#----s11-------
l0,lerr0=offset(CCD1='s4',CCD2='s11',cat=cat,xadd=40,yadd=0,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s4s11.png')
pl.close()
l1,lerr1=offset(CCD1='s11',CCD2='s4',cat=cat,xadd=-40,yadd=0,sep=70,crit_f=5)
pl.savefig(baseDir+'figure/s11s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s11')[0])
y.append(ccd_offset('s4','s11')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s11')

#----s12-------
l0,lerr0=offset(CCD1='s4',CCD2='s12',cat=cat,xadd=40,yadd=-100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s4s12.png')
pl.close()
l1,lerr1=offset(CCD1='s12',CCD2='s4',cat=cat,xadd=-40,yadd=100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s12s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s12')[0])
y.append(ccd_offset('s4','s12')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s12')


#----s13-------

l0,lerr0=offset(CCD1='s4',CCD2='s13',cat=cat,xadd=20,yadd=-100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s4s13.png')
pl.close()
l1,lerr1=offset(CCD1='s13',CCD2='s4',cat=cat,xadd=-20,yadd=100,sep=70,crit_f=10)
pl.savefig(baseDir+'figure/s13s4.png')
pl.close()
zm=(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.
x.append(ccd_offset('s4','s13')[0])
y.append(ccd_offset('s4','s13')[1])
z.append(zm)
zerr.append(zmerr)
name.append('s13')




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
p=np.array([0.00062,-0.001909,-0.0366])#result from Tom
zoffset=z-plane(p,x,y)

plane(p,x,y)



c1=pf.Column(name='x',format='D',array=x)
c2=pf.Column(name='y',format='D',array=y)
c3=pf.Column(name='z',format='D',array=z)
c4=pf.Column(name='zerr',format='D',array=zerr)
c5=pf.Column(name='zoffset',format='D',array=zoffset)
c6=pf.Column(name='CCD',format='10A',array=name)

hdu=pf.new_table([c1,c2,c3,c4,c5,c6])
hdu.writeto('flatness_8_30_10.fit')




"""
----analysis----

x=pf.getdata('flatness_8_30_10.fit').field('x')
y=pf.getdata('flatness_8_30_10.fit').field('y')
z=pf.getdata('flatness_8_30_10.fit').field('z')
zerr=pf.getdata('flatness_8_30_10.fit').field('zerr')
zoffset=pf.getdata('flatness_8_30_10.fit').field('zoffset')
name=pf.getdata('flatness_8_30_10.fit').field('CCD')


pl.plot(np.arange(len(name)),zoffset,'b.')
pl.errorbar(np.arange(len(name)),zoffset,yerr=zerr,ecolor='b',fmt='.')
pl.xticks(np.arange(len(name)),name)
pl.hlines(np.median(zoffset),-1,len(name)+2,'r')
pl.hlines(np.median(zoffset)+2.,-1,len(name)+2,'g',linestyles='dashed')
pl.hlines(np.median(zoffset)-2.,-1,len(name)+2,'g',linestyles='dashed')
pl.xlim(-1,len(name)+2)
pl.ylim(np.median(zoffset)-4,np.median(zoffset)+4)
pl.ylabel('offset (pixels)')
pl.xlabel('CCDs')


scale=2048.
xx=x/scale
yy=y/scale
zz=z/5.
zzoffset=zoffset/5.

barchart(xx,yy,zz)
barchart(xx,yy,zzoffset)


#----plot the extracted image-----
ext=np.array([27,28,29,5,6,7,8,4,3,2,1,31,30,34,9,10,11,12])
for i in range(len(ext)):
    b=pf.getdata(cat[i])
    f=b.field('FLUX_BEST')
    ok=f>=320000
    ra=b.field('X_WORLD')[ok]
    dec=b.field('Y_WORLD')[ok]
    x,y=wcs2pix(ra,dec)
    pl.plot(x,-y,'b.')

tmp=pf.open(baseDir+'bias/Image_flatness_bias.fits')
tmp.verify('silentfix')
for i in range(len(ext)):
    b=pf.getdata(check[i])
    tmp[ext[i]].data=b
    print i

tmp.writeto(baseDir+'figure/check_all.fits')


"""
