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


def single_dark(NameFits=None,Channel=None):
    num=len(NameFits) 
    imgl=pf.getdata(NameFits[0],Channel)[2800:3000,700:800]
    imgr=pf.getdata(NameFits[0],Channel)[2800:3000,1500:1800]
    for i in range(1,num):
        imgl=[imgl,pf.getdata(NameFits[i],Channel)[2800:3000,700:800]]
        imgr=[imgr,pf.getdata(NameFits[i],Channel)[2800:3000,1500:1800]]
        imgl=np.median(imgl,axis=0)
        imgr=np.median(imgr,axis=0)
    detector = pf.open(NameFits[0])[Channel].header['DETSER']
    imgl.flatten()
    imgr.flatten()
    mnl=robust_mean(imgl)
    rmsl=robust_std(imgl)
    mnr=robust_mean(imgr)
    rmsr=robust_std(imgr)
    fig=pl.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,2,1)
    bins=np.arange(round(mnl-10),round(mnl+10),1)
    pl.hist(imgl,bins=bins)
    pl.xlim(mnl-4*rmsl,mnl+4*rmsl)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'left')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnl,2))+r'$\pm$'+str(round(rmsl,2))+' (ADU)',transform = ax.transAxes)   
    ax=fig.add_subplot(1,2,2)
    bins=np.arange(round(mnr-10),round(mnr+10),1)
    pl.hist(imgr,bins=bins)
    pl.xlim(mnr-4*rmsr,mnr+4*rmsr)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'right')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnr,2))+r'$\pm$'+str(round(rmsr,2))+' (ADU)',transform = ax.transAxes)
    return(detector)

#-----main programme-------------

dir='/data.02/dark_imager_8_13_10/'  
NameFits=gl.glob(dir+'*.fits')
NameFits.sort()
NameBias=dir+'bias/Image_dark_002136.fits'
num=len(NameFits)
for i in range(num):
    print i
    subName=NameFits[i][:-5]+'_bias_sub.fits'
    t=Img_sub(NameFits[i],NameBias,subName)



NameFits=gl.glob(dir+'*sub*.fits')
ext=[1,2,3,4,5,6,7,8,9,10,11,12,27,28,29,30,31,34]
for i in ext:
    print i
    det=single_dark(NameFits,Channel=i)
    #det=dark_sispi(NameFits,NameBias,Channel=i)
    pl.savefig(dir+'fig/dark_current'+'_'+det+'_ext_'+str(i)+'.png')
    pl.close()
    



