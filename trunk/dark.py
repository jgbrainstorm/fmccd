#! /usr/bin/env python
from fermiMCCD import *

def dark_sispi(NameFits=None,NameBias=None,Channel=None):
    img=pf.getdata(NameFits,Channel)
    bias=pf.getdata(NameBias,Channel)
    bins=np.arange(-20,20,1)
    imgl= img[2800:3000,700:800] - bias[2800:3000,700:800]
    imgr= img[2800:3000,1500:1800] - bias[2800:3000,1500:1800]
    detector = pf.open(NameBias)[Channel].header['DETSER']
    imgl.flatten()
    imgr.flatten()
    mnl=robust_mean(imgl)
    rmsl=robust_std(imgl)
    mnr=robust_mean(imgr)
    rmsr=robust_std(imgr)
    fig=pl.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,2,1)
    pl.hist(imgl,bins=bins)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'left')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnl,2))+r'$\pm$'+str(round(rmsl,2))+' (ADU)',transform = ax.transAxes)   
    ax=fig.add_subplot(1,2,2)
    pl.hist(imgr,bins=bins)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'right')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnr,2))+r'$\pm$'+str(round(rmsr,2))+' (ADU)',transform = ax.transAxes)
    return(detector)


#-----main programme-------------

dir='/data.02/dark_imager_8_13_10/'
    
NameFits=dir+'Image_dark_002137.fits'
NameBias=dir+'Image_dark_002136.fits'

ext=[1,2,3,4,5,6,7,8,9,10,11,12,27,28,29,30,31,34]
for i in ext:
    print i
    det=dark_sispi(NameFits,NameBias,Channel=i)
    pl.savefig(dir+'dark_current'+'_'+det+'_ext_'+str(i)+'.png')
    pl.close()
    



