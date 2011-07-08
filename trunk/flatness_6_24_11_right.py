#!/usr/bin/env python
# examine the flatness
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *

    
#step 1: set the directory


baseDir = '/data/jiangang/flatness_6_24_11/rightside/'


#step2: separate extensions to files 


NameFits=gl.glob(baseDir+'*.fits')
NameFits.sort()

ccd=['s22','s21','s20','s14','s15','s16','s10','s9','s8','s1','s2','s3','s4','n4','n3','n2','n1','n8','n9','n10','n16','n15','n14','n20','n21','n22']

ext=['i22s','i21s','i20s','i14s','i15s','i16s','i10s','i9s','i8s','i1s','i2s','i3s','i4s','i4n','i3n','i2n','i1n','i8n','i9n','i10n','i16n','i15n','i14n','i20n','i21n','i22n']

fileNo=range(len(ccd))
ccd2fileNo=dict(zip(ccd,fileNo))



for i in range(len(ext)):
    t=extract_extension(NameFits[i],ext[i])


NameBias=baseDir+'bias/bias.fits'
for i in range(len(ext)):
    t=extract_extension(NameBias,ext[i])



#step 2: subtract the bias by extension

NameExt=gl.glob(baseDir+'*exten*.fits')
NameExt.sort()

for i in range(len(ext)):
    hdu=pf.open(NameExt[i])
    bias=pf.getdata(baseDir+'bias/bias_exten_'+ext[i]+'.fits')
    hdu[0].data = hdu[0].data - bias
    hdu[0].header.update('CTYPE2', 'DEC--TAN')
    hdu[0].header.update('CTYPE1', 'RA--TAN')    
    output=NameExt[i][0:-5]+'_sub.fits'
    hdu.writeto(output)





#step 3: extract catalog

name = gl.glob(baseDir+'*sub.fits')
name.sort()
Nfile=len(name)
sexdir='/home/jghao/software/sextractor-2.5.0/config/'

for i in range(Nfile):
        img_name=name[i]
        output=img_name[0:-5]+'_catalog.fits'
        ckimg=img_name[0:-5]+'check.fits'
	t=sex(img_name,output,thresh=2.0,fwhm=4,gain=None,zmag=None,sexdir=sexdir,scale=0.125,check_img=ckimg,sigma_map=None,config="default.sex")
	
        #t=sex(img_name,output,thresh=2.0,fwhm=4,gain=None,zmag=None,sexdir=sexdir,scale=0.125,check_img=ckimg,sigma_map=None,config="photdes.config")



# step 4:-----analyze the files---------------
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *
baseDir = '/data/jiangang/flatness_6_24_11/rightside/'
cat=gl.glob(baseDir+'Image_*catalog.fits')
cat.sort()


l0,lerr0=offset(CCD1='n10',CCD2='n4',cat=cat,xadd=60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n4',CCD2='n10',cat=cat,xadd=-60,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s4',cat=cat,xadd=40,yadd=10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s4',CCD2='n4',cat=cat,xadd=-40,yadd=-10,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s10',cat=cat,xadd=80,yadd=40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s10',CCD2='n4',cat=cat,xadd=-80,yadd=-40,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s9',cat=cat,xadd=80,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s9',CCD2='n4',cat=cat,xadd=-80,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s3',cat=cat,xadd=30,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s3',CCD2='n4',cat=cat,xadd=-30,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='n3',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n3',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='n9',cat=cat,xadd=-50,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n9',CCD2='n4',cat=cat,xadd=50,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='n2',cat=cat,xadd=0,yadd=60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n2',CCD2='n4',cat=cat,xadd=0,yadd=-60,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s2',cat=cat,xadd=30,yadd=80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s2',CCD2='n4',cat=cat,xadd=-30,yadd=-80,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s8',cat=cat,xadd=80,yadd=90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s8',CCD2='n4',cat=cat,xadd=-80,yadd=-90,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='s1',cat=cat,xadd=30,yadd=120,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='s1',CCD2='n4',cat=cat,xadd=-30,yadd=-120,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='n1',cat=cat,xadd=-10,yadd=100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n1',CCD2='n4',cat=cat,xadd=10,yadd=-100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)

l0,lerr0=offset(CCD1='n4',CCD2='n8',cat=cat,xadd=-50,yadd=100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n8',CCD2='n4',cat=cat,xadd=50,yadd=-100,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)











#--------plot everything-------------

ext=['i22s','i21s','i20s','i14s','i15s','i16s','i10s','i9s','i8s','i1s','i2s','i3s','i4s','i4n','i3n','i2n','i1n','i8n','i9n','i10n','i16n','i15n','i14n','i20n','i21n','i22n']
pl.plot(0,0,'ro')
tmp=pf.open(baseDir+'bias/bias.fits')

for i in range(len(ext)):
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


























