#!/usr/bin/env python
# examine the flatness
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *

#step 1: set the directory

baseDir = '/data/jiangang/flat_allccd_7_8_11/upperright/'


#step2: separate extensions to files

NameFits=gl.glob(baseDir+'*.fits')
NameFits.sort()

ccd=['s30','s29','s25','s26','s22','s21','s20','s14','s15','s16','s10','s9','s8','s1','s2','s3','s4','n4','n3','n2','n1']

ext=['i30s','i29s','i25s','i26s','i22s','i21s','i20s','i14s','i15s','i16s','i10s','i9s','i8s','i1s','i2s','i3s','i4s','i4n','i3n','i2n','i1n']

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
	
 


# step 4:-----analyze the files---------------
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *
baseDir = '/data/jiangang/flatness_6_24_11/leftside/'
cat=gl.glob(baseDir+'Image_*catalog.fits')
cat.sort()



l0,lerr0=offset(CCD1='n11',CCD2='n4',cat=cat,xadd=50,yadd=0,sep=70,crit_f=50,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset(CCD1='n4',CCD2='n11',cat=cat,xadd=-50,yadd=0,sep=70,crit_f=50,ccd2fileNo=ccd2fileNo)







#--------plot everything-------------
ext=np.array(['i11n','i4n','i4s','i11s','i12s','i5s','i5n','i12n','i6n','i6s','i13s','i7s','i7n','i13n'])

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


























