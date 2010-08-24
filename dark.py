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
    imgl=pf.getdata(NameFits[0],Channel)[2800:3000,700:900]
    imgr=pf.getdata(NameFits[0],Channel)[2800:3000,1500:1700]
    totalIMGL=np.zeros((num,imgl.shape[0],imgl.shape[1]))
    totalIMGR=np.zeros((num,imgr.shape[0],imgr.shape[1]))
    totalIMGL[0,:,:]=imgl
    totalIMGR[0,:,:]=imgr
    for j in range(1,num):
        totalIMGL[j,:,:]=pf.getdata(NameFits[j],Channel)[2800:3000,700:900]
        totalIMGR[j,:,:]=pf.getdata(NameFits[j],Channel)[2800:3000,1500:1700]
    imgl=np.median(totalIMGL,axis=0)
    imgr=np.median(totalIMGR,axis=0)
    totalIMGL=0  # release mem.
    totalIMGR=0
    detector = pf.open(NameFits[0])[Channel].header['DETSER']
    imgl=imgl.flatten()
    imgr=imgr.flatten()
    mnl=np.mean(imgl)
    rmsl=np.std(imgl)
    mnr=np.mean(imgr)
    rmsr=np.std(imgr)
    fig=pl.figure(figsize=(15,7.5))
    ax=fig.add_subplot(1,2,1)
    bins=np.arange(round(mnl-10),round(mnl+10),1)
    pl.hist(imgl,bins=bins)
    #pl.xlim(mnl-4*rmsl,mnl+4*rmsl)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'left')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnl,2))+r'$\pm$'+str(round(rmsl,2))+' (ADU)',transform = ax.transAxes)
    pl.text(0.1,0.85,'Total pix #: '+str(len(imgl)),transform = ax.transAxes)
    pl.text(0.1,0.8,'# of pix > 0: '+str(len(imgl[imgl>0])),transform = ax.transAxes)
    pl.text(0.1,0.75,'# of pix > 1: '+str(len(imgl[imgl>1])),transform = ax.transAxes)
    ax=fig.add_subplot(1,2,2)
    bins=np.arange(round(mnr-10),round(mnr+10),1)
    pl.hist(imgr,bins=bins)
    #pl.xlim(mnr-4*rmsr,mnr+4*rmsr)
    pl.title('Position:' +detector+'     Channel: '+str(Channel)+'right')
    pl.text(0.1,0.9,'Dark Current:'+str(round(mnr,2))+r'$\pm$'+str(round(rmsr,2))+' (ADU)',transform = ax.transAxes)
    pl.text(0.1,0.85,'Total pix #: '+str(len(imgr)),transform = ax.transAxes)
    pl.text(0.1,0.8,'# of pix > 0: '+str(len(imgr[imgr>0])),transform = ax.transAxes)
    pl.text(0.1,0.75,'# of pix > 1: '+str(len(imgr[imgr>1])),transform = ax.transAxes) 
    return(detector)

#-----main programme-------------
"""
dir='/data.02/dark_imager_8_13_10/'  
NameFits=gl.glob(dir+'*.fits')
NameFits.sort()
NameBias=dir+'bias/Image_dark_002136.fits'
num=len(NameFits)
for i in range(num):
    print i
    subName=NameFits[i][:-5]+'_bias_sub.fits'
    t=Img_sub(NameFits[i],NameBias,subName)
"""

dir='/data.02/dark_imager_8_13_10/'  
NameFits=gl.glob(dir+'*sub*.fits')
ext=[1,2,3,4,5,6,7,8,9,10,11,12,27,28,29,30,31,34]
for i in ext:
    print i
    det=single_dark(NameFits,Channel=i)
    #det=dark_sispi(NameFits,NameBias,Channel=i)
    pl.savefig(dir+'fig/dark_current'+'_'+det+'_ext_'+str(i)+'.png')
    pl.close()
    



