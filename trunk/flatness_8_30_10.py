#!/usr/bin/env python
# examine the flatness

from fermiMCCD import *  
#import sexPy as sx
#import flatpy as fl

#step 0: subtract bias images
dir = '/data.02/flat_8_30_10/'
NameFits=gl.glob('*.fits')
NameFits.sort()
NameBias=dir+'bias/Image_flatness_bias.fits'
num=len(NameFits)
for i in range(num):
    print i
    subName=NameFits[i][:-5]+'_bias_sub.fits'
    t=Img_sub(NameFits[i],NameBias,subName)

    
#step 1: set the directory


baseDir = '/data.02/flat_8_30_10/'


#step2: separate extensions to files (this is done manually, see notebook for mapping the ext number and file name)
NameFits=gl.glob(baseDir+'*sub.fits')
NameFits.sort()
ext=np.array([27,28,29,5,6,7,8,4,3,2,1,31,30,34,9,10,11,12])
for i in range(len(NameFits)):
    t=extract_ext(NameFits[i],ext[i])


#step 3: extract catalog

name = gl.glob(baseDir+'Image_flat_*_exten_*.fits')
name.sort()
Nfile=len(name)
sexdir='/home/jghao/software/sextractor-2.5.0/config/'

for i in range(Nfile):
        img_name=name[i]
        output=img_name[0:-5]+'_catalog.fits'
        ckimg=img_name[0:-5]+'check.fits'
	t=sex(img_name,output,thresh=2.0,fwhm=4,gain=None,zmag=None,sexdir=sexdir,scale=0.125,check_img=ckimg,sigma_map=None,config="default.sex")
	
        #t=sex(img_name,output,thresh=2.0,fwhm=4,gain=None,zmag=None,sexdir=sexdir,scale=0.125,check_img=ckimg,sigma_map=None,config="photdes.config")




#step 4: the data

cat=gl.glob(baseDir+'Image_*catalog.fits')
cat.sort()


#------0680,0681,0682, 0697 to check the repeatibility of S12---

b0=pf.getdata(cat[0])
b1=pf.getdata(cat[1])
b2=pf.getdata(cat[2])
b3=pf.getdata(cat[17])

f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')
f2=b2.field('FLUX_BEST')
f3=b3.field('FLUX_BEST')

ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)
ok2=f2>np.mean(f2)
ok3=f3>np.mean(f3)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]
ra2=b2.field('X_WORLD')[ok2]
dec2=b2.field('Y_WORLD')[ok2]
ra3=b3.field('X_WORLD')[ok3]
dec3=b3.field('Y_WORLD')[ok3]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)
y2,x2=wcs2pix(ra2,dec2)
y3,x3=wcs2pix(ra3,dec3)

in1,in2=xy_matching(xa=x0,ya=y0,xb=x1,yb=y1,sep=2)
match_analysis(xa=x0,ya=y0,xb=x1,yb=y1,ina=in1,inb=in2)

in1,in2=xy_matching(xa=x0,ya=y0,xb=x2,yb=y2,sep=2)
match_analysis(xa=x0,ya=y0,xb=x2,yb=y2,ina=in1,inb=in2)

in1,in2=xy_matching(xa=x0,ya=y0,xb=x3,yb=y3,sep=2)
match_analysis(xa=x0,ya=y0,xb=x3,yb=y3,ina=in1,inb=in2)

in1,in2=xy_matching(xa=x1,ya=y1,xb=x2,yb=y2,sep=2)
match_analysis(xa=x1,ya=y1,xb=x2,yb=y2,ina=in1,inb=in2)

in1,in2=xy_matching(xa=x1,ya=y1,xb=x3,yb=y3,sep=2)
match_analysis(xa=x1,ya=y1,xb=x3,yb=y3,ina=in1,inb=in2)



#------0683,85 check the repeatibility of S17---

b0=pf.getdata(cat[3])
b1=pf.getdata(cat[5])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)


ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=xy_matching(xa=x0,ya=y0,xb=x1,yb=y1,sep=2)

match_analysis(xa=x0,ya=y0,xb=x1,yb=y1,ina=in1,inb=in2)


#------0684,0686 check the repeatibility of S23---

b0=pf.getdata(cat[4])
b1=pf.getdata(cat[6])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=xy_matching(xa=x0,ya=y0,xb=x1,yb=y1,sep=2)
match_analysis(xa=x0,ya=y0,xb=x1,yb=y1,ina=in1,inb=in2)


#---------match S2 and S3-----


b0=pf.getdata(cat[1])
b1=pf.getdata(cat[2])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='s2',xa=x0,ya=y0,CCD2='s3',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)
ccd_match_offset(CCD1='2S',xa=x0,ya=y0,CCD2='3S',xb=x1,yb=y1,ina=in1,inb=in2)





#---------match N4 and N6-----


b0=pf.getdata(cat[7])
b1=pf.getdata(cat[9])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n4',xa=x0,ya=y0,CCD2='n6',xb=x1,yb=y1,xadd=0,yadd=-150,sep=90)
ccd_match_offset(CCD1='N4',xa=x0,ya=y0,CCD2='N6',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=-150)


#---------match N4 and N5-----


b0=pf.getdata(cat[7])
b1=pf.getdata(cat[8])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n4',xa=x0,ya=y0,CCD2='n5',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)

ccd_match_offset(CCD1='N4',xa=x0,ya=y0,CCD2='N5',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)





#---------match N5 and N4-----


b0=pf.getdata(cat[8])
b1=pf.getdata(cat[7])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n5',xa=x0,ya=y0,CCD2='n4',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)

ccd_match_offset(CCD1='N5',xa=x0,ya=y0,CCD2='N4',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)




#---------match N5 and N6-----


b0=pf.getdata(cat[8])
b1=pf.getdata(cat[9])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n5',xa=x0,ya=y0,CCD2='n6',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)
ccd_match_offset(CCD1='N5',xa=x0,ya=y0,CCD2='N6',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)



#---------match N6 and N5-----


b0=pf.getdata(cat[9])
b1=pf.getdata(cat[8])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n6',xa=x0,ya=y0,CCD2='n5',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)
ccd_match_offset(CCD1='N6',xa=x0,ya=y0,CCD2='N5',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)








#---------match N6 and N7-----


b0=pf.getdata(cat[9])
b1=pf.getdata(cat[10])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n6',xa=x0,ya=y0,CCD2='n7',xb=x1,yb=y1,xadd=0,yadd=0,sep=50)
ccd_match_offset(CCD1='n6',xa=x0,ya=y0,CCD2='n7',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)


#---------match N4 and N7-----


b0=pf.getdata(cat[7])
b1=pf.getdata(cat[10])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='n4',xa=x0,ya=y0,CCD2='n7',xb=x1,yb=y1,xadd=20,yadd=0,sep=80)
ccd_match_offset(CCD1='n4',xa=x0,ya=y0,CCD2='n7',xb=x1,yb=y1,ina=in1,inb=in2,xadd=20,yadd=0)

#---------match S4 and S5-----


b0=pf.getdata(cat[11])
b1=pf.getdata(cat[12])


f0=b0.field('FLUX_BEST')
f1=b1.field('FLUX_BEST')


ok0=f0>np.mean(f0)
ok1=f1>np.mean(f1)

ra0=b0.field('X_WORLD')[ok0]
dec0=b0.field('Y_WORLD')[ok0]
ra1=b1.field('X_WORLD')[ok1]
dec1=b1.field('Y_WORLD')[ok1]

y0,x0=wcs2pix(ra0,dec0)
y1,x1=wcs2pix(ra1,dec1)

in1,in2=ccd_match(CCD1='s4',xa=x0,ya=y0,CCD2='s5',xb=x1,yb=y1,xadd=0,yadd=0,sep=80)
ccd_match_offset(CCD1='s4',xa=x0,ya=y0,CCD2='s5',xb=x1,yb=y1,ina=in1,inb=in2,xadd=0,yadd=0)






#-----analyze the files---------------

from fermiMCCD import *
baseDir = '/data.02/flat_8_21_10/'
cat=gl.glob(baseDir+'Image_*catalog.fits')
cat.sort()


l0,lerr0=offset(CCD1='s2',CCD2='s3',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n4_n5_offset.pdf')
l1,lerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n5_n4_offset.pdf')
(l0-l1)/2., (lerr0+lerr1)/2.



l0,lerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n4_n6_offset.pdf')
l1,lerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=150,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n6_n4_offset.pdf')
(l0-l1)/2., (lerr0+lerr1)/2.




l0,lerr0=offset(CCD1='n5',CCD2='n6',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n5_n6_offset.pdf')
l1,lerr1=offset(CCD1='n6',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n6_n5_offset.pdf')
(l0-l1)/2., (lerr0+lerr1)/2.




#------------measurement for all ccds w.r.t. N4-------------------
l0,lerr0=offset(CCD1='n4',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)


l0,lerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=150,sep=70,crit_f=30)


l0,lerr0=offset(CCD1='n4',CCD2='n7',cat=cat,xadd=30,yadd=-170,sep=70,crit_f=80)
l1,lerr1=offset(CCD1='n7',CCD2='n4',cat=cat,xadd=-30,yadd=170,sep=70,crit_f=80)


l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)

l0,lerr0=offset(CCD1='n4',CCD2='s5',cat=cat,xadd=0,yadd=0,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=80,crit_f=30)


l0,lerr0=offset(CCD1='n4',CCD2='s6',cat=cat,xadd=80,yadd=-100,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s6',CCD2='n4',cat=cat,xadd=-80,yadd=100,sep=80,crit_f=30)

l0,lerr0=offset(CCD1='n4',CCD2='s7',cat=cat,xadd=100,yadd=-150,sep=80,crit_f=30)
l1,lerr1=offset(CCD1='s7',CCD2='n4',cat=cat,xadd=-100,yadd=150,sep=80,crit_f=30)


l0,lerr0=offset(CCD1='n4',CCD2='s10',cat=cat,xadd=100,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s10',CCD2='n4',cat=cat,xadd=-100,yadd=0,sep=70,crit_f=8)


l0,lerr0=offset(CCD1='n4',CCD2='s11',cat=cat,xadd=100,yadd=20,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s11',CCD2='n4',cat=cat,xadd=-100,yadd=-20,sep=70,crit_f=20)


l0,lerr0=offset(CCD1='n4',CCD2='s12',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=8)
l1,lerr1=offset(CCD1='s12',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=8)


l0,lerr0=offset(CCD1='n4',CCD2='s13',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s13',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s16',cat=cat,xadd=100,yadd=-150,sep=70,crit_f=20)#not very good
l1,lerr1=offset(CCD1='s16',CCD2='n4',cat=cat,xadd=-100,yadd=150,sep=70,crit_f=20)


l0,lerr0=offset(CCD1='n4',CCD2='s17',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s17',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s18',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s18',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)


l0,lerr0=offset(CCD1='n4',CCD2='s19',cat=cat,xadd=100,yadd=-100,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s19',CCD2='n4',cat=cat,xadd=-100,yadd=100,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s21',cat=cat,xadd=100,yadd=-1200,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s21',CCD2='n4',cat=cat,xadd=-100,yadd=1200,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s22',cat=cat,xadd=100,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s22',CCD2='n4',cat=cat,xadd=-100,yadd=0,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s23',cat=cat,xadd=150,yadd=-50,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s23',CCD2='n4',cat=cat,xadd=-150,yadd=50,sep=70,crit_f=10)


l0,lerr0=offset(CCD1='n4',CCD2='s24',cat=cat,xadd=200,yadd=-150,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s24',CCD2='n4',cat=cat,xadd=-200,yadd=150,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s26',cat=cat,xadd=200,yadd=-50,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s26',CCD2='n4',cat=cat,xadd=-200,yadd=50,sep=70,crit_f=10)

l0,lerr0=offset(CCD1='n4',CCD2='s27',cat=cat,xadd=200,yadd=0,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s27',CCD2='n4',cat=cat,xadd=-200,yadd=0,sep=70,crit_f=10)


l0,lerr0=offset(CCD1='n4',CCD2='s28',cat=cat,xadd=200,yadd=-50,sep=70,crit_f=30)
l1,lerr1=offset(CCD1='s28',CCD2='n4',cat=cat,xadd=-200,yadd=50,sep=70,crit_f=30)

l0,lerr0=offset(CCD1='n4',CCD2='s29',cat=cat,xadd=200,yadd=-1250,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s29',CCD2='n4',cat=cat,xadd=-200,yadd=1250,sep=70,crit_f=20)

l0,lerr0=offset(CCD1='n4',CCD2='s30',cat=cat,xadd=200,yadd=0,sep=70,crit_f=20)
l1,lerr1=offset(CCD1='s30',CCD2='n4',cat=cat,xadd=-200,yadd=0,sep=70,crit_f=20)

l0,lerr0=offset(CCD1='n4',CCD2='s31',cat=cat,xadd=250,yadd=-270,sep=70,crit_f=10)
l1,lerr1=offset(CCD1='s31',CCD2='n4',cat=cat,xadd=-250,yadd=270,sep=70,crit_f=10)









"""

x0,xerr0,y0,yerr0=offset(CCD1='n4',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n4_n5_offset.pdf')
x1,xerr1,y1,yerr1=offset(CCD1='n5',CCD2='n4',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n5_n4_offset.pdf')
(x0-x1)/2., (xerr0+xerr1)/2.,(y0-y1)/2., (yerr0+yerr1)/2.


x0,xerr0,y0,yerr0=offset(CCD1='n4',CCD2='n6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n4_n6_offset.pdf')
x1,xerr1,y1,yerr1=offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=150,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n6_n4_offset.pdf')
(x0-x1)/2., (xerr0+xerr1)/2.,(y0-y1)/2., (yerr0+yerr1)/2.


x0,xerr0,y0,yerr0=offset(CCD1='n5',CCD2='n6',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n5_n6_offset.pdf')
x1,xerr1,y1,yerr1=offset(CCD1='n6',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
pl.savefig('/home/jghao/research/SPIE2010/fig/n6_n5_offset.pdf')
(x0-x1)/2., (xerr0+xerr1)/2.,(y0-y1)/2., (yerr0+yerr1)/2.



x0,xerr0,y0,yerr0=offset(CCD1='n6',CCD2='n7',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
x1,xerr1,y1,yerr1=offset(CCD1='n7',CCD2='n6',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)
(x0-x1)/2., (xerr0-xerr1)/2.,(y0-y1)/2., (yerr0-yerr1)/2.





offset(CCD1='n5',CCD2='n7',cat=cat,xadd=0,yadd=0,sep=150,crit_f=30)
offset(CCD1='n7',CCD2='n5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)




offset(CCD1='s4',CCD2='s5',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)

offset(CCD1='s5',CCD2='s6',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)

offset(CCD1='s4',CCD2='s6',cat=cat,xadd=0,yadd=-150,sep=70,crit_f=40)

offset(CCD1='n6',CCD2='n4',cat=cat,xadd=0,yadd=150,sep=70,crit_f=0)

offset(CCD1='n6',CCD2='n7',cat=cat,xadd=0,yadd=0,sep=70,crit_f=30)

"""




#---------intrinsic tilt-for S-17, file 33-38--------

ccd_tilt(CCD='s17',cat=cat,fileNoa=33,fileNob=34,xadd=0,yadd=-333.,sep=40,crit_f=10,dd=333.)
pl.savefig('/home/jghao/research/SPIE2010/fig/s17_tilt_1.pdf')
ccd_tilt(CCD='s17',cat=cat,fileNoa=33,fileNob=35,xadd=0,yadd=-333*2.,sep=40,crit_f=10,dd=333.*2)
pl.savefig('/home/jghao/research/SPIE2010/fig/s17_tilt_2.pdf')
ccd_tilt(CCD='s17',cat=cat,fileNoa=33,fileNob=36,xadd=0,yadd=-333*3.,sep=40,crit_f=10,dd=333.*3)
pl.savefig('/home/jghao/research/SPIE2010/fig/s17_tilt_3.pdf')
#ccd_tilt(CCD='s17',cat=cat,fileNoa=33,fileNob=37,xadd=0,yadd=-333*4.,sep=40,crit_f=5,dd=333.*4)
#pl.savefig('/home/jghao/research/SPIE2010/fig/s17_tilt_4.eps')
ccd_tilt(CCD='s17',cat=cat,fileNoa=33,fileNob=38,xadd=0,yadd=-333*5.,sep=40,crit_f=5,dd=333.*5)
pl.savefig('/home/jghao/research/SPIE2010/fig/s17_tilt_4.pdf')

ccd_tilt(CCD='s17',cat=cat,fileNoa=34,fileNob=38,xadd=0,yadd=-333*4.,sep=40,crit_f=5,dd=333.*4)


#--------plot everything-------------

ext=range(7,33)
pl.plot(0,0,'ro')
tmp=pf.open(baseDir+'bias/median.fits')

for i in ext:
	b=pf.getdata(cat[i])
	f=b.field('FLUX_BEST')
        ok=f>=np.mean(f)
	ra=b.field('X_WORLD')[ok]
	dec=b.field('Y_WORLD')[ok]
        x,y=wcs2pix(ra,dec)
	pl.plot(x,y,'b.')
	


for i in ext:
	b=pf.getdata(check[i])
	tmp[i-6].data=b
	print i

tmp.writeto(baseDir+'check_mosaic.fits')


























