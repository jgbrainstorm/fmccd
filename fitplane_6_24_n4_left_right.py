#

from fermiMCCD import *
from scipy.optimize import leastsq
from enthought.mayavi.mlab import *

cat =[]
cat.append('/home/jghao/research/ccd/imager/flatness_6_24_11/leftside/Image_fltleft47_00028687_exten_i4n_sub_catalog.fits')
cat.append('/home/jghao/research/ccd/imager/flatness_6_24_11/rightside/Image_fltright47_00028654_exten_i4n_sub_catalog.fits')

ccd2fileNo={'n4_l':0, 'n4_r':1}


l0,lerr0=offset_LR(CCD1='n4_l',CCD2='n4_r',cat=cat,xadd=0,yadd=0,sep=170,crit_f=0,ccd2fileNo=ccd2fileNo)
l1,lerr1=offset_LR(CCD1='n17',CCD2='n4',cat=cat,xadd=100,yadd=0,sep=70,crit_f=0,ccd2fileNo=ccd2fileNo)
zm=abs(l0-l1)/2.
zmerr=abs(lerr0+lerr1)/2.

