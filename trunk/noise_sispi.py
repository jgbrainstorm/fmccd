#! /usr/bin/env python
from fermiMCCD import *
dirbase='/data.02/linearity_imager_ionpump_on_8_11_10/'


#-----bkp1--------------
dir=dirbase+'bkp1/'
NameBias=gl.glob(dir+'bias/image*.fits')
NameBias.sort()
NameBias = NameBias[3]

hdu=pf.open(NameBias)
Channel=[1,2,3,4,5,8]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=1)
         print ns
         pl.savefig(dir+'fig/bkp1_noise_channel_'+str(i)+'_left.png')	
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=0)
         print ns
         pl.savefig(dir+'fig/bkp1_noise_channel_'+str(i)+'_right.png')

#------bkp3-----------
dir=dirbase+'bkp3/'
NameBias=gl.glob(dir+'bias/image*.fits')
NameBias.sort()
NameBias = NameBias[3]


hdu=pf.open(NameBias)
Channel=[1,2,3,4]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=1)
         print ns
         pl.savefig(dir+'fig/bkp3_noise_channel_'+str(i)+'_left.png')	
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=0)
         print ns
         pl.savefig(dir+'fig/bkp3_noise_channel_'+str(i)+'_right.png')

		


#------bkp4----------------

dir=dirbase+'bkp4/'
NameBias=gl.glob(dir+'bias/image*.fits')
NameBias.sort()
NameBias = NameBias[3]

hdu=pf.open(NameBias)
Channel=[1,2,3,4,5,6,7,8]
#Channel=np.arange(1,len(hdu))
for i in Channel:
         print i
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=1)
         print ns
         pl.savefig(dir+'fig/bkp4_noise_channel_'+str(i)+'_left.png')	
         ns=noise_channel_sispi(NameBias,i,plot=1,shift=0,left=0)
         print ns
         pl.savefig(dir+'fig/bkp4_noise_channel_'+str(i)+'_right.png')

           
     
