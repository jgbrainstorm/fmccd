#! /usr/bin/env python
from fermiMCCD import *

dirbase='/data.02/linearity_imager_ionpump_on_8_11_10/'

#-----bkp1--------------
dir=dirbase+'bkp1/'
NameFits=gl.glob(dir+'/image*.fits')
NameBias=dir+'/bias/median.fits'
NameFits.sort()

hdu=pf.open(NameBias)
Channel=[1,2,3,4,5,8]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         linearity(NameFits,NameBias,i,shift=0,left=1)
         pl.savefig(dir+'fig/bkp1_linearity_channel_'+str(i)+'_left.png')	
         linearity(NameFits,NameBias,i,shift=0,left=0)
         pl.savefig(dir+'fig/bkp1_linearity_channel_'+str(i)+'_right.png')

#------bkp3-----------
dir=dirbase+'bkp3/'
NameFits=gl.glob(dir+'/image*.fits')
NameBias=dir+'/bias/median.fits'
NameFits.sort()

hdu=pf.open(NameBias)
Channel=[1,2,3,4]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         linearity(NameFits,NameBias,i,shift=0,left=1)
         pl.savefig(dir+'fig/bkp3_linearity_channel_'+str(i)+'_left.png')	
         linearity(NameFits,NameBias,i,shift=0,left=0)
         pl.savefig(dir+'fig/bkp3_linearity_channel_'+str(i)+'_right.png')
		

#------bkp4----------------

dir=dirbase+'bkp4/'
NameFits=gl.glob(dir+'/image*.fits')
NameBias=dir+'/bias/median.fits'
NameFits.sort()

hdu=pf.open(NameBias)
Channel=[1,2,3,4,5,6,7,8]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         linearity(NameFits,NameBias,i,shift=0,left=1)
         pl.savefig(dir+'fig/bkp4_linearity_channel_'+str(i)+'_left.png')	
         linearity(NameFits,NameBias,i,shift=0,left=0)
         pl.savefig(dir+'fig/bkp4_linearity_channel_'+str(i)+'_right.png')
		
