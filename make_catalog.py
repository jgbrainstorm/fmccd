#! /usr/bin/env python
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *

ext=np.array([2,3,5,41,42,38,39,8,19,20,21])

#catdir='/data/10Jan2011_0deg/hexpodmove_tilt/'
catdir='/data/jiangang/zenith/hexpod_move/'
NameFits=gl.glob(catdir+'*.fits')
Nfits=len(NameFits)
for i in range(Nfits):
    for j in ext:
        t=extract_ext(NameFits[i],j)

name = gl.glob('*_exten_*.fits')
name.sort()
Nfile=len(name)
sexdir='/home/jghao/software/sextractor-2.5.0/config/'

for i in range(Nfile):
        img_name=name[i]
        output=img_name[0:-5]+'_catalog.fits'
        ckimg=img_name[0:-5]+'check.fits'
	t=sex(img_name,output,thresh=3.,fwhm=4,gain=None,zmag=None,sexdir=sexdir,scale=0.27,check_img=ckimg,sigma_map=None,config="default.sex")
	
os.system('mv '+'*catalog*.fits '+catdir+'catalog/')
os.system('rm *exten*.fits')
