"""
This package is aimed at reducing the MultiCCD images produced from the MCCDTV for Dark Energy Survey at Fermilab. 

Dependencies: pyfits, numpy, matplotlib

Jiangang Hao
10/18/2009

"""


import pylab as pl
import numpy as np
import pyfits as pf
import glob as gl
import os
import sys
import string
import scipy.optimize as op
from fermiMCCD_def import *
import scipy.stats.kde as ke
from scipy.stats import kstest

#----gaussfit-----------------


def kde(x=None,range=None):
    x=x[(x>=range[0])*(x<=range[1])]
    res=ke.gaussian_kde(x)
    

#-----Robust Mean--------------
def robust_mean(x):
    y = x.flatten()
    if len(np.unique(y))==1:
        meany=y[0]
    else:
        n = len(y)
        y.sort()
        ind_qt1 = round((n+1)/4.)
        ind_qt3 = round((n+1)*3/4.)
        IQR = y[ind_qt3]- y[ind_qt1]
        lowFense = y[ind_qt1] - 1.5*IQR
        highFense = y[ind_qt3] + 1.5*IQR
        if lowFense == highFense:
            meany=lowFense
        else:
            ok = (y>lowFense)*(y<highFense)
            yy=y[ok]
            meany=yy.mean(dtype='double')
    return meany


#-------Robust Standard Deviation---

def robust_std(x):
    y = x.flatten()
    if len(np.unique(y))==0:
        stdy=0.
    else:
        n = len(y)
        y.sort()
        ind_qt1 = round((n+1)/4.)
        ind_qt3 = round((n+1)*3/4.)
        IQR = y[ind_qt3]- y[ind_qt1]
        lowFense = y[ind_qt1] - 1.5*IQR
        highFense = y[ind_qt3] + 1.5*IQR
        if lowFense == highFense:
            stdy=lowFense
        else:
            ok = (y>lowFense)*(y<highFense)
            yy=y[ok]
            stdy=yy.std(dtype='double')
    return stdy

#-------weighted mean, std--------
def wmean(x,xerr):
    w=1./(xerr**2)
    wm=sum(x*w)/sum(w)
    return(wm)


def wsd(x,xerr):
    w=1./(xerr**2)
    ws=np.sqrt(1./sum(w))
    return(ws)




#-------Robust variance---

def robust_var(x):
    y = x.flatten()
    if len(np.unique(y))==0:
        vary=0.
    else:
        n = len(y)
        y.sort()
        ind_qt1 = round((n+1)/4.)
        ind_qt3 = round((n+1)*3/4.)
        IQR = y[ind_qt3]- y[ind_qt1]
        lowFense = y[ind_qt1] - 1.5*IQR
        highFense = y[ind_qt3] + 1.5*IQR
        if lowFense == highFense:
            vary=lowFense
        else:
            ok = (y>lowFense)*(y<highFense)
            yy=y[ok]
            vary=yy.var(dtype='double')
    return vary


#--------some binned plots-----
def histhao(x,bsize=None):
    nbin=(np.max(x)-np.min(x))/bsize
    d=np.histogram(x,bins=nbin)
    return d


def bin_scatter(x,y,yerr=None,binsize=None):
    h=histhao(x,binsize) 
    nbin=len(h[0])
    xm=np.zeros(nbin)
    ym=np.zeros(nbin)
    sdym=np.zeros(nbin)
    for i in range(0,len(h[0])):
        ind=(x>=h[1][i])*(x<h[1][i+1])
        tt=x[ind]
        if len(tt) > 0:
            xm[i]=np.mean(x[ind])
            if yerr:
                ym[i]=wmean(y[ind],yerr[ind])
                sdym[i]=wsd(y[ind],yerr[ind])
            else:
                ym[i]=np.mean(y[ind])
                sdym[i]=np.std(y[ind])/np.sqrt(len(y[ind]))     
    pl.errorbar(xm,ym,yerr=sdym,fmt='ro')





#----line fit------------------------
"""
y = a+bx.
input:  y, x
return: a,b, sd_a, sd_b, R^2
This is used where there is no measurement errors on x, y
http://mathworld.wolfram.com/LeastSquaresFitting.html
http://en.wikipedia.org/wiki/R-squared
"""

def linefit(x,y):
    """
    a,b,SEa,SEb,chi2 = linefit(x)
    """
    n=len(x)
    SSxx = n*np.var(x,dtype='double')
    SSyy = n*np.var(y,dtype='double')
    ybar = np.mean(y,dtype='double')
    xbar = np.mean(x,dtype='double')
    SSxy = np.sum(x*y,dtype='double') - n*xbar*ybar
    b = SSxy/SSxx
    a = ybar - b*xbar
    s = np.sqrt((SSyy-SSxy**2/SSxx)/(n-2))
    SEa = s*np.sqrt(1/n+xbar**2/SSxx)
    SEb = s/np.sqrt(SSxx)
    SStot = np.sum((y-ybar)**2,dtype='double')
    f = a + b*x
    SSerr = np.sum((y-f)**2,dtype='double')
    Rsq = 1-SSerr/SStot
    return a,b,SEa,SEb,Rsq


#---weighted LSQ fit to straightline based on NR---
""" 
y = a +b x, 
input:  x, y, yerr
return: a, b, sd_a, sd_b, chi2
See NR chapter 15
"""

def linfit(xx,yy,yyerr):
    if len(yy[np.abs(yy)>0]) < 10:
        b=0
        a=0
        SEa=0
        SEb=0
        chi2=999
        return a,b,SEa,SEb,chi2
    else:
        ok=yyerr > 0
        x = xx[ok]
        y = yy[ok]
        yerr = yyerr[ok]
        n=len(x)
        S=np.sum(1/yerr**2,dtype='double')
        Sx = np.sum(x/yerr**2,dtype='double')
        Sy = np.sum(y/yerr**2,dtype='double')
        Sxx = np.sum(x**2/yerr**2,dtype='double')
        Sxy = np.sum((x*y)/(yerr**2),dtype='double')
        delta = S*Sxx - Sx**2
        a = (Sxx*Sy-Sx*Sxy)/delta
        b = (S*Sxy-Sx*Sy)/delta
        SEa = np.sqrt(Sxx/delta)
        SEb = np.sqrt(S/delta)
        chi2 = np.sum((y-(a + b*x))**2/yerr**2,dtype='double')/(n-2.)
        return a,b,SEa,SEb,chi2

        

def binner(x=None,y=None,yerr=None,binsize=None):
    h=histhao(x,binsize) 
    nbin=len(h[0])
    xm=np.zeros(nbin)
    ym=np.zeros(nbin)
    sdym=np.zeros(nbin)
    for i in range(0,len(h[0])):
        ind=(x>=h[1][i])*(x<h[1][i+1])
        tt=x[ind]
        if len(tt) > 0:
            xm[i]=np.median(x[ind])
            if yerr:
                ym[i]=wmean(y[ind],yerr[ind])
                sdym[i]=wsd(y[ind],yerr[ind])
            else:
                ym[i]=np.mean(y[ind])
                sdym[i]=np.std(y[ind])/np.sqrt(len(y[ind]))
    return xm,ym,sdym


def binlinfit(x,y,bsize):
    xx,yy,yyerr = binner(x,y,binsize=bsize)
    (a,b,SEa,SEb,chi2)=linfit(xx,yy,yyerr)
    return a,b,SEa,SEb,chi2


def mode_gauss(x,binsize=None,range=None,crit_f=None):
    bins=(range[1]-range[0])/np.float(binsize)
    hist,bin_edge=np.histogram(x,bins=bins,range=range)
    ok=np.argwhere(hist >= crit_f)
    xok=(x>bin_edge[ok.min()])*(x<=bin_edge[ok.max()+1])
    mean=robust_mean(x[xok])
    stdm=robust_std(x[xok])/np.sqrt(len(xok))
    ks,p = kstest(x[xok],'norm')
    return mean,stdm,ks,p

#-----scale CCD image to int16-------
"""
Calling: newHDU=scaleHDU(HDU)

"""

def scaleHDU(x):
    hdu = x
    exterN = len(hdu)
    for i in range(0,exterN):
        hdu[i].scale('int16','',bzero=32768)
    return hdu


#-----reflect the image with column/row symmetry-----
"""
reflect a given image/matrix by colum/row.
if row=1 then reflect w.r.t. row
if col=1 then reflect w.r.t. col
call: img=reflectImg(imgo,row=None,col=None)
return: the reflected image/matrix

"""

def reflectImg(imgo,row=None,col=None):
    img = imgo
    xsize = img.shape[1]  # col
    ysize = img.shape[0]  # row
    imgNew = np.zeros((ysize,xsize))
    if row == 1:
        for i in range(0,ysize):
           
            imgNew[i,:] = img[ysize-1-i,:]
    if col == 1:
        for j in range(0,xsize):
            imgNew[:,j] = img[:,xsize-1-j]
    return imgNew


#-------make the median image of multi-extension images-----
"""
Calculate the median image of multi-extension image file
Input: directory of the images, File head of the image file
       name of the median image (default is median.fits)
Call: median
Output: a median image file is created in the directory you specified.
Return: the median HDU
"""
def median_Img(dir=None,fileHEAD=None,medianName=None):
    if dir is None:
        dir=os.getcwd()
        dir=dir+'/'
        imagName=gl.glob(dir+'*.fits')
    else:
        imagName = gl.glob(dir+fileHEAD+'*.fits')       
    medianHDU = pf.open(imagName[0])
    medianHDU.verify('silentfix')
    NChannel = len(medianHDU)
    Nfile =len(imagName)
    totalIMG = np.zeros((Nfile,medianHDU[1].data.shape[0],medianHDU[1].data.shape[1]),dtype=int)
    for i in range(1,NChannel):     # i runs for channel
        for j in range(0,Nfile):    # j runs for file
            totalIMG[j,:,:] =pf.getdata(imagName[j],i)
        medianHDU[i].data = np.median(totalIMG,axis=0)
        print 'extension: ', i
    HDU = scaleHDU(medianHDU)
    if medianName:
        HDU.writeto(dir+medianName)
    else:
        HDU.writeto(dir+'median.fits')
    return(HDU)



#-------read ccd images----------------------

def readCCDFits(NameFits,Channel):
    hdu = pf.open(NameFits)
    data = hdu[Channel].data
    hdr = hdu[Channel].header
    return data,hdr

#------substract two images, normal used for bias substraction---------

def Img_subtraction(imageHDU=None,biasHDU=None,subName=None):
    NChannel = len(imageHDU)
    for i in range(1,NChannel):
        imageHDU[i].data = imageHDU[i].data - biasHDU[i].data
   # HDU = scaleHDU(medianHDU) """ scale the image"""
    HDU = imageHDU
    if subName != None:
        HDU.writeto(subName)
    
    return(HDU)


def Img_sub(imageName=None,biasName=None,subName=None):
    if subName:
        imageHDU=pf.open(imageName)
        imageHDU.verify('silentfix')
        NChannel=len(imageHDU)
        for i in range(1,NChannel):
            imageHDU[i].data=pf.getdata(imageName,i)-pf.getdata(biasName,i)
        imageHDU=scaleHDU(imageHDU)
        imageHDU.writeto(subName)
    else:
        imageHDU=pf.open(imageName,mode='update')
        NChannel = len(imageHDU)
        for i in range(1,NChannel):
            imageHDU[i].data=pf.getdata(imageName,i)-pf.getdata(biasName,i)
        imageHDU=scaleHDU(imageHDU)
        imageHDU.flush()    
        return(0)





#------subtract the overscan-------

def subOscan(hdu):
    n=len(hdu)
    for i in range(1,n):
        col0=hdu[i].header['biassec'].split('[')[1].split(']')[0].split(',')[0].split(':')[0]
        col1=hdu[i].header['biassec'].split('[')[1].split(']')[0].split(',')[0].split(':')[1]
        row0=hdu[i].header['biassec'].split('[')[1].split(']')[0].split(',')[1].split(':')[0]
        row1=hdu[i].header['biassec'].split('[')[1].split(']')[0].split(',')[1].split(':')[1]
        oscan=hdu[i].data[int(row0)-1:int(row1),int(col0)-1:int(col1)]       
        md=np.median(oscan,axis=1)
        row=np.arange(0,md.shape[0])
        (a,b,sda,sdb,se)=linefit(row,md)
        value=row*b+a
        col0=hdu[i].header['datasec'].split('[')[1].split(']')[0].split(',')[0].split(':')[0]
        col1=hdu[i].header['datasec'].split('[')[1].split(']')[0].split(',')[0].split(':')[1]
        row0=hdu[i].header['datasec'].split('[')[1].split(']')[0].split(',')[1].split(':')[0]
        row1=hdu[i].header['datasec'].split('[')[1].split(']')[0].split(',')[1].split(':')[1]
        valueM=np.zeros((4096,1024))
        for k in range(1024):
		valueM[:,k] = value
        hdu[i].data[int(row0)-1:int(row1),int(col0)-1:int(col1)]-valueM
    return(hdu)
 

def master_bias(dir=None,fileHEAD=None,medianName=None):
    if dir is None:
        dir=os.getcwd()
        dir=dir+'/'
        imagName=gl.glob(dir+'*.fits')
    else:
        imagName = gl.glob(dir+fileHEAD+'*.fits')
        
    medianHDU = pf.open(imagName[0])
    NChannel = len(medianHDU)
    Nfile = len(imagName)
    totalIMG = np.zeros((Nfile,medianHDU[1].data.shape[0],medianHDU[1].data.shape[1]))
    for i in range(1,NChannel):     # i runs for channel
        for j in range(0,Nfile):    # j runs for file
            HDU = pf.open(imagName[j]) 
            imagHDU=subOscan(HDU)         
            totalIMG[j,:,:] = imagHDU[i].data
        medianHDU[i].data = np.median(totalIMG,axis=0)
        print 'extension: ', i
    HDU = scaleHDU(medianHDU)
    if medianName:
        HDU.writeto(dir+medianName)
    else:
        HDU.writeto(dir+'masterBias.fits')
    return(HDU)






#---------image reduction---------------------
#--this function do the bias subtraction -----

def image_reduction_oscan(dir=None,biasName=None):
    if dir is None:
        dir=os.getcwd()
        dir=dir+'/'
        imagName=gl.glob(dir+'*.fits')
    else:
        imagName = gl.glob(dir+'*.fits')
    if biasName is None:
	biasName=dir+'/bias/median.fits'
    Nfile = len(imagName)
    bias = pf.open(biasName)
    for i in range(0,Nfile):
        img=pf.open(imagName[i],mode='update')
        img=subOscan(img)
        NChannel=len(img)
        print i
        for j in range(1,NChannel):
            img[j].data=img[j].data-bias[j].data
        img=scaleHDU(img)
        #img.writeto(imagName[i][:-5]+'_bias_sub.fits')
        img.flush()


#---------image reduction---------------------
#--this function do the bias subtraction -----

def image_reduction(dir=None,biasName=None):
    if dir is None:
        dir=os.getcwd()
        dir=dir+'/'
        imagName=gl.glob(dir+'*.fits')
    else:
        imagName = gl.glob(dir+'*.fits')
    if biasName is None:
	biasName=dir+'/bias/median.fits'
    Nfile = len(imagName)
    bias = pf.open(biasName)
    for i in range(0,Nfile):
        img=pf.open(imagName[i],mode='update')
        #img=subOscan(img)
        NChannel=len(img)
        print i
        for j in range(1,NChannel):
            img[j].data=img[j].data-bias[j].data
        img=scaleHDU(img)
        #img.writeto(imagName[i][:-5]+'_bias_sub.fits')
        img.flush()



def linearity(NameFits,NameBias,Channel,shift=None,left=None):

    if left == None or left == 1:
        #colmin=150
        #colmax=350
        colmin=300
        colmax=800
        #rowmin=200 #lower
        #rowmax=500
        #xmin=2000 #middle
        #xmax=2500    
        #xmin=3600 #upper
        #xmax=4000
        rowmin=100  #new region
        rowmax=200
    else:
        #colmin=1300
        #colmax=1750
        colmin=1300
        colmax=1800
        #rowmin=200
        #rowmax=500
        rowmin=100
        rowmax=200
    #the following change is due to the bad part on the new CCD mounted 4/15/2010.
    detector = pf.open(NameBias)[Channel].header['DETSER']
    if detector[-1]=='N':
        rowmin=3946
        rowmax=4046
       
    if shift == 1:
        colshift = np.random.random_integers(0,500,1)
        rowshift = np.random.random_integers(0,3000,1)
        rowmin = rowmin + rowshift
        rowmax = rowmax + rowshift
        colmin = colmin + colshift
        colmax = colmax + colshift
    NFile = len(NameFits)
    num = round((NFile-1)/2.)
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    exptime=np.zeros(num)
    #exptime=np.arange(5,130,5)
    #exptime=np.append(np.arange(0,0.4,0.04),np.arange(0.02,0.46,0.04))
    
    for i in range(0,num):
        bias,biashdr = readCCDFits(NameBias,Channel)
        bias = bias[rowmin:rowmax,colmin:colmax]
        ba,hdra = readCCDFits(NameFits[i*2],Channel)
        ba = ba[rowmin:rowmax,colmin:colmax]
        ba = ba - bias
        bb,hdrb = readCCDFits(NameFits[i*2+1],Channel)
        bb = bb[rowmin:rowmax,colmin:colmax]
        bb = bb - bias
        uni = np.unique(ba)
        add_b = ba + bb
        diff_b= ba - bb
        mean_b[i] = robust_mean(add_b)/2.
        var_b[i] = robust_var(diff_b)/2.
        exptime[i]=pf.open(NameFits[i*2])[0].header['EXPTIME']        
        #exptime[i]=i*5
        ok = (mean_b > 0)*(mean_b <20000)*(var_b < 8000)          
        if len(mean_b[ok]) > 2:
            (a,b,SEa,SEb,R2) = linefit(mean_b[ok],var_b[ok])
            gain = b
            (ta,tb,tSEa,tSEb,tR2) = linefit(exptime[ok],mean_b[ok])           
        else:
            gain=999
            a=0
            b=0
            SEb=999
            ta=0
            tb=0
            tSEa=999
            tSEb=999
        
    fig=pl.figure(figsize=(15,15))
    #pl.subplot(2,2,1)
    ax=fig.add_subplot(2,2,1)
    pl.plot(exptime,mean_b,'bo')
    pl.hold(True)
    pl.plot(exptime[0:5],exptime[0:5]*tb+ta,'r-')
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Bias subtracted mean counts (ADU)')
    if left == None:
        pl.title('Position:' +detector+'     Channel: '+str(Channel))
    if left == 1:
        pl.title('Position:' +detector+'     Channel: '+str(Channel)+' left')
    if left == 0:
        pl.title('Position:' +detector+'     Channel: '+str(Channel)+' right')
    ax=fig.add_subplot(2,2,2)
    dff=(mean_b-(tb*exptime+ta))/(tb*exptime+ta)
    uuu=mean_b[abs(dff) <= 0.01]
    if uuu.any() == True:
        ffwid=mean_b==max(uuu)
        ffw=mean_b[ffwid]
    else:
        ffw=999
        ffwid=0
    pl.plot(exptime,dff,'bo')
    pl.plot(exptime[ffwid],dff[ffwid],'ro')
    pl.hold(True)
    pl.hlines(0.01,0,300,colors='r',linestyles='dashed')
    pl.hlines(-0.01,0,300,colors='r',linestyles='dashed')
    pl.ylim(-0.05,0.05)
    pl.xlim(min(exptime),max(exptime))
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Relative deviation from the fitted line')    
    pl.text(0.1,0.9,'Fullwell:'+str(round(ffw))+' (ADU)',transform = ax.transAxes)
    pl.text(0.1,0.85,'Fullwell:'+str(round(ffw/gain))+' (e-)',transform = ax.transAxes) 
    ax=fig.add_subplot(2,2,3)
    pl.plot(mean_b,var_b,'bo')
    pl.xlim(0,60000)
    pl.hold(True)
    pl.plot(np.array([0,36000]),np.array([0,36000])*b+a,'r-')
    pl.text(0.1,0.9,'Gain:'+str(round(np.mean(gain),5))+'$\pm$'+str(round(np.mean(SEb),5)),transform = ax.transAxes)
    pl.ylim(-1,18000)
    pl.xlim(-1,60000)
    pl.xlabel('Bias subtracted mean counts (ADU)')
    pl.ylabel('Variance (ADU)')
    ax=fig.add_subplot(2,2,4)
    diff=(var_b-(b*mean_b+a))/(b*mean_b+a)
    uu=mean_b[abs(diff) <= 0.1]
    if uu.any() == True:
        fwid=mean_b==max(uu)
        fw=mean_b[fwid]
    else:
        fw=999
        fwid=0
    print fw
    pl.plot(mean_b,diff,'bo')
    pl.plot(fw,diff[fwid],'ro')
    pl.hold(True)
    pl.hlines(0.1,0,60000,colors='r',linestyles='dashed')
    pl.hlines(-0.1,0,60000,colors='r',linestyles='dashed')
    pl.ylim(-1,1)
    pl.text(0.1,0.9,'Fullwell:'+str(round(fw))+' (ADU)',transform = ax.transAxes)
    pl.text(0.1,0.85,'Fullwell:'+str(round(fw/gain))+' (e-)',transform = ax.transAxes)
    pl.xlabel('Bias subtracted mean counts (ADU)')
    pl.ylabel('Relative deviation from the fitted line')    



   
#-----for single CCD readout data from the cube---
def linearity_single(NameFits,NameBias,shift=None):
    ymin=150
    ymax=350
    xmin=500 
    xmax=800
    if shift == 1:
        yshift = np.random.random_integers(0,500,1)
        xshift = np.random.random_integers(0,3000,1)
        xmin = xmin + xshift
        xmax = xmax + xshift
        ymin = ymin + yshift
        ymax = ymax + yshift
    NFile = len(NameFits)
    num = round((NFile-1)/4.)
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    exptime=np.zeros(num)
    for i in range(0,num):
        print i
        bias= pf.getdata(NameBias[0])
        bias = bias[xmin:xmax,ymin:ymax]
        ba = pf.getdata(NameFits[i*4+1])
        ba = ba[xmin:xmax,ymin:ymax]
        ba = ba - bias
        bb = pf.getdata(NameFits[i*4+3])
        bb = bb[xmin:xmax,ymin:ymax]
        bb = bb - bias
        add_b = ba + bb
        diff_b= ba - bb
        mean_b[i] = robust_mean(add_b)/2
        var_b[i] = robust_var(diff_b)/2
        exptime[i]=10*i
    ok = (mean_b > 0)*(mean_b <150000)
    (a,b,SEa,SEb,R2) = linefit(mean_b[ok],var_b[ok])
    gain = b
    fig=pl.figure(figsize=(15,5))
    pl.subplot(1,2,1)
    ax=fig.add_subplot(1,2,1)
    pl.plot(exptime,mean_b,'bo')
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Bias subtracted mean counts (ADU)')
    pl.title('Linearity plot for Single CCD')
    ax=fig.add_subplot(1,2,2)
    pl.plot(mean_b,var_b,'bo',a)
    pl.hold(True)
    pl.plot(np.array([0,360000]),np.array([0,360000])*b+a,'r-')
    pl.text(0.1,0.9,'Gain:'+str(round(np.mean(gain),5))+'$\pm$'+str(round(np.mean(SEb),5)),transform = ax.transAxes)
    pl.ylim(-1,230000)
    pl.xlim(-1,230000)
    pl.xlabel('Bias subtracted mean counts (ADU)')
    pl.ylabel('Variance (ADU)')
   

def linearity_sandstorm(NameFits,NameBias,shift=None):
    xmin=550   # row
    xmax=850
    ymin=1500  #col
    ymax=1800
    if shift == 1:
        yshift = np.random.random_integers(0,500,1)
        xshift = np.random.random_integers(0,3000,1)
        xmin = xmin + xshift
        xmax = xmax + xshift
        ymin = ymin + yshift
        ymax = ymax + yshift
    NFile = len(NameFits)
    num = round((NFile-1)/4.)
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    exptime=np.zeros(num)
    for i in range(0,num):
        print i
        bias= pf.getdata(NameBias[0])
        bias = bias[xmin:xmax,ymin:ymax]
        ba = pf.getdata(NameFits[i*2])
        ba = ba[xmin:xmax,ymin:ymax]
        ba = ba - bias
        bb = pf.getdata(NameFits[i*2+1])
        bb = bb[xmin:xmax,ymin:ymax]
        bb = bb - bias
        add_b = ba + bb
        diff_b= ba - bb
        mean_b[i] = robust_mean(add_b)/2
        var_b[i] = robust_var(diff_b)/2
        exptime[i]=10*i
    ok = (mean_b > 0)*(mean_b <1500000)
    (a,b,SEa,SEb,R2) = linefit(mean_b[ok],var_b[ok])
    gain = b
    fig=pl.figure(figsize=(15,5))
    pl.subplot(1,2,1)
    ax=fig.add_subplot(1,2,1)
    pl.plot(exptime,mean_b,'bo')
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Bias subtracted mean counts (ADU)')
    pl.title('Linearity plot for Single CCD')
    ax=fig.add_subplot(1,2,2)
    pl.plot(mean_b,var_b,'bo',a)
    pl.hold(True)
    pl.plot(np.array([0,2600000]),np.array([0,2600000])*b+a,'r-')
    pl.text(0.1,0.9,'Gain:'+str(round(np.mean(gain),5))+'$\pm$'+str(round(np.mean(SEb),5)),transform = ax.transAxes)
    pl.ylim(-1,2300000)
    pl.xlim(-1,2300000)
    pl.xlabel('Bias subtracted mean counts (ADU)')
    pl.ylabel('Variance (ADU)')
 


# the distribution of gain when using random window
def gain_distribution(NameFits,NameBias,Channel,plot=None,figdir=None):

    Nrpt = 50
    gainArray = np.zeros(Nrpt)

    for i in range(0,Nrpt):
        gainArray[i] = gain_channel(NameFits,NameBias,Channel,shift=1,plot=0,figdir=figdir)

    if plot == 1:

        pl.hist(gainArray,10)
        pl.xlabel('Gain Distribution')
        pl.show()
    
    return gainArray



#---------------------------------------------------
# Calculate the readout noise on the overscan region
#---------------------------------------------------

def noise_channel(NameFits,Channel,plot=None,shift=None):

    left = np.mod(Channel,2)
    if left == 1:
        ncolmin=15
      	ncolmax=50
      	nrowmin=500
      	nrowmax=700
    else:   
        ncolmin=1025
      	ncolmax=1074
      	nrowmin=500
      	nrowmax=700
    if shift == 1:
        nxshift = np.random.random_integers(0,3000,1)
        nxmin = nxmin + nxshift
        nxmax = nxmax + nxshift

    noisea,hdrn = readCCDFits(NameFits,Channel)
    nois = noisea[nrowmin:nrowmax,ncolmin:ncolmax]

    uni = np.unique(nois)

    if len(uni) < 10:
        
        return 'N/A'
    elif plot == 1:
        pl.hist(nois,10,facecolor='green')
        pl.xlabel('Pixel Values in Overscan (ADU)')
        pl.title('Readout Noise for Channel:'+str(Channel))
        pl.legend(('Mean:'+str(robust_mean(nois)),'Sd:'+str(robust_std(nois))))
        pl.xlim(robust_mean(nois)-5*robust_std(nois), robust_mean(nois)+5*robust_std(nois))
     #   pl.savefig(figdir+'noise_'+hdrn[17]+str(left)+'.png')
     #  pl.show()
     #   pl.close()
        return robust_std(nois)
    else:
        return robust_std(nois)
    

#---------------------------------------------------
# Calculate the readout noise based on random window
#---------------------------------------------------

def noise_distribution(NameFits,NameBias,Channel,plot=None,figdir=None):
    Nrpt=50
    gainArray = np.zeros(Nrpt)

    for i in range(0,Nrpt):
        noiseArray[i] = noise_channel(NameFits,NameBias,Channel,shift=1,plot=0,figdir=figdir)

    if plot == 1:

        pl.hist(gainArray,10)
        pl.xlabel('Noise Distribution (ADU)')
        pl.show()
    
    return gainArray

#---xtalk calculate xtalk coefficients------

def xtalk(imageHDU=None,sourceCH=None,victimCH=None,winSg=None,winBg=None,NamePng = None):
      
    HDUlist = imageHDU
    NChannel = len(HDUlist)

    colmin = winSg[0]
    colmax = winSg[1]
    rowmin = winSg[2]
    rowmax = winSg[3]
   
    colminBg = winBg[0]    # for background substraction
    colmaxBg = winBg[1]
    rowminBg = winBg[2]
    rowmaxBg = winBg[3]
    
    lefts = np.mod(sourceCH,2)
    leftv = np.mod(victimCH,2)

    imgS = HDUlist[sourceCH].data
    bgimgS = np.median(HDUlist[sourceCH].data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgS = imgS[rowmin:rowmax,colmin:colmax] - bgimgS

    imgV = HDUlist[victimCH].data
    
    if lefts != leftv:
        imgV = reflectImg(imgV,col=1)
        
    bgimgV = np.median(HDUlist[victimCH].data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgV = imgV[rowmin:rowmax,colmin:colmax] - bgimgV
    
    sso = imgS
    vvo = imgV
    
    ss=sso.reshape(sso.shape[0]*sso.shape[1])
    vv=vvo.reshape(vvo.shape[0]*vvo.shape[1])

    idd = (ss > 35000)*(ss < 65000)
    ss=ss[idd]
    vv=vv[idd]
    vverr = np.sqrt(np.abs(vv))

    #(a,b,SEa,SEb,Rsq) = linefit(ss,vv)
    (a,b,SEa,SEb,chi2) = linfit(ss,vv,vverr)
    pl.figure(figsize=(15, 10))
    pl.subplot(2,2,1)
    #pl.contourf(sso)
    pl.imshow(sso,origin='lower')
    pl.title('Channel: '+str(sourceCH))
    pl.subplot(2,2,2)
   # pl.contourf(vvo)
    pl.imshow(vvo,origin='lower')
    pl.title('Channel: '+str(victimCH))
    pl.subplot(2,2,3)
    pl.plot(ss,vv,'b.',ss,b*ss+a,'-k',linewidth=2)
    pl.xlabel('Source Image')
    pl.ylabel('Victim Image')
    pl.title('Cross-talk Coefficient:'+str(np.round(b,6))+'('+str(np.round(SEb,6))+')'+'('+str(round(chi2,1))+')')
   # pl.title('Cross-talk Coefficient:'+str(np.round(b,6))+'('+str(np.round(SEb,6))+')')
    pl.subplot(2,2,4)
   # pl.contourf(vvo-b*sso-a)
    pl.imshow(vvo-b*sso-a,origin='lower')
    pl.title('Corrected Victim(Channel:'+str(victimCH)+')')

    if NamePng != None:
        pl.savefig(NamePng+'xtalk_'+str(sourceCH)+'_'+str(victimCH)+'.png')
    else:
        pl.show()
    
    return(b)

    

#----- light tight check----
def dark_comp(channel=None):
    dir='/data/22Jul2009_light_tight/'
    im=pf.open(dir+'median.fits')[channel].data
    im = im - np.median(im[20:70,200:800])
    print '23th(60 second exp):',np.median(im.flat)
    dir='/data/23Jul2009_light_tight/'
    im=pf.open(dir+'median.fits')[channel].data
    im = im - np.median(im[20:70,200:800])
    print '23th(10 second exp):',np.median(im.flat)
    return(0)


#-------calculate dark current-----
def dark_current(imgHDU=None,biasHDU=None,Channel=None,pngName=None):
    left = np.mod(Channel,2)
    img = imgHDU[Channel].data
    bias = biasHDU[Channel].data
    if left == 1:
        nymin=15
      	nymax=50
      	nxmin=1000
      	nxmax=2000
    else:   
        nymin=1050
      	nymax=1100
      	nxmin=1000
      	nxmax=2000
    osnImg = img[nxmin:nxmax,nymin:nymax]    
    osnBias = img[nxmin:nxmax,nymin:nymax]
    img = img - np.median(osnImg)
    bias = bias - np.median(osnBias)
    dark = img - bias
    rms=robust_std(dark)
    mn = np.median(dark)
    pl.hist(dark.flat,bins=1000,range=[-40,40])
    pl.title("Dark Current for 60 sec exposure: Channel "+str(Channel))
    pl.xlabel("Median: "+str(round(mn,3))+", RMS: "+str(round(rms,3))+" (ADU)")
    pl.savefig(pngName)
    pl.close()
    return mn, rms



#---auto xtalk coef---------
def xcoeff(imgNumber=None,source=None,victim=None,winSg=None,winBg=None,NamePng=None):

    rowmin = winSg[0]
    rowmax = winSg[1]
    colmin = winSg[2]
    colmax = winSg[3]

    rowminBg = winBg[0]
    rowmaxBg = winBg[1]   
    colminBg = winBg[2]    # for background substraction
    colmaxBg = winBg[3]
    
    lefts = np.mod(source.ext,2)
    leftv = np.mod(victim.ext,2)
    source.loaddata(imgNumber)
    victim.loaddata(imgNumber)
    imgS = source.data
    bgimgS = np.median(source.data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgS = imgS[rowmin:rowmax,colmin:colmax] - bgimgS

    imgV = victim.data
    
    if lefts != leftv:
        imgV = reflectImg(imgV,col=1)
        
    bgimgV = np.median(victim.data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgV = imgV[rowmin:rowmax,colmin:colmax] - bgimgV
    
    sso = imgS
    vvo = imgV
    
    ss=sso.reshape(sso.shape[0]*sso.shape[1])
    vv=vvo.reshape(vvo.shape[0]*vvo.shape[1])

    idd = (ss > 35000)*(ss < 65000)
    ss=ss[idd]
    vv=vv[idd]
    #(a,b,SEa,SEb,chi2)=binlinfit(ss,vv,2000)
    vverr = np.sqrt(np.abs(vv))
    (a,b,SEa,SEb,chi2) = linfit(ss,vv,vverr)
    pl.figure(figsize=(15, 10))
    pl.subplot(2,2,1)

    pl.imshow(sso,origin='lower')
    pl.title('Source: '+source.pos)
    pl.subplot(2,2,2)

    pl.imshow(vvo,origin='lower')
    pl.title('Victim: '+victim.pos)
    pl.subplot(2,2,3)
    pl.hold(True)
    pl.plot(sso,vvo,'b.')
    #bin_scatter(ss,vv,binsize=2000)
    pl.plot(np.array([10000,65000]),np.array([10000,65000])*b+a,'r-')
    pl.vlines(35000,-100,100,color='green',linestyles='dashed')
    pl.xlabel('Source (ADU)')
    pl.ylabel('Victim (ADU)')
    pl.title('Xtalk Coefficient:'+str(np.round(b,7))+'$\pm$'+str(np.round(SEb,7))+'('+str(round(chi2,1))+')')
    pl.subplot(2,2,4)
    pl.imshow(vvo-b*sso-a,origin='lower')
    pl.title('Corrected Victim '+victim.pos)

    if NamePng != None:
        pl.savefig(NamePng+'xtalk_'+source.pos+'_'+victim.pos+'.png')
        pl.close()
    else:
        pl.show()
    
    return(b)


def xcoeff_hist(imgNumber=None,source=None,victim=None,winSg=None,winBg=None,NamePng=None):

    rowmin = winSg[0]
    rowmax = winSg[1]
    colmin = winSg[2]
    colmax = winSg[3]

    rowminBg = winBg[0]
    rowmaxBg = winBg[1]   
    colminBg = winBg[2]    # for background substraction
    colmaxBg = winBg[3]
    
    lefts = np.mod(source.ext,2)
    leftv = np.mod(victim.ext,2)
    source.loaddata(imgNumber)
    victim.loaddata(imgNumber)
    imgS = source.data
    bgimgS = np.median(source.data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgS = imgS[rowmin:rowmax,colmin:colmax] - bgimgS

    imgV = victim.data
    
    if lefts != leftv:
        imgV = reflectImg(imgV,col=1)
        
    bgimgV = np.median(victim.data[rowminBg:rowmaxBg,colminBg:colmaxBg])
    imgV = imgV[rowmin:rowmax,colmin:colmax] - bgimgV
    
    sso = imgS
    vvo = imgV
    
    ss=sso.reshape(sso.shape[0]*sso.shape[1])
    vv=vvo.reshape(vvo.shape[0]*vvo.shape[1])

    idd = (ss > 35000)*(ss < 65000)
    if(len(np.unique(ss[idd])) > 10)*(len(np.unique(vv[idd])) > 5):
        ss=ss[idd]
        vv=vv[idd]
        xcof=vv*1./ss
        b=robust_mean(xcof)
        pl.figure(figsize=(15, 10))
        pl.subplot(2,2,1)
        pl.imshow(sso,origin='lower')
        pl.title('Source: '+source.pos)
        pl.subplot(2,2,2)
        pl.imshow(vvo,origin='lower')
        pl.title('Victim: '+victim.pos)
        pl.subplot(2,2,3)
        pl.hold(True)
        pl.boxplot(xcof)
        pl.title('Xtalk Coefficient:'+str(np.round(b,7))+'$\pm$'+str(np.round(robust_std(xcof),7)))
        b=np.round(b,7)
        pl.subplot(2,2,4)
        pl.imshow(vvo-b*sso,origin='lower')
        pl.title('Corrected Victim '+victim.pos)
        if NamePng != None:
            pl.savefig(NamePng+'xtalk_'+source.pos+'_'+victim.pos+'.png')
            pl.close()
        else:
            pl.show()
    else:
        pl.figure(figsize=(15, 10))
        pl.subplot(2,2,1)
        pl.imshow(sso,origin='lower')
        pl.title('Source: '+source.pos)
        pl.subplot(2,2,2)
        pl.imshow(vvo,origin='lower')
        pl.title('Victim: '+victim.pos)
        b=0
        if NamePng != None:
            pl.savefig(NamePng+'xtalk_'+source.pos+'_'+victim.pos+'.png')
            pl.close()
        else:
            pl.show()
    return(b)


#-------sextractor -------------------

def sex(image, output, thresh=None, fwhm=None, gain=None, zmag=None,
        sexdir='/Users/burns/CSP/template_subtraction/sex', scale=0.125, check_img=None, sigma_map=None,config=None):
   '''Construct a sextractor command and run it.'''
   if sexdir[-1] != '/':  sexdir += '/'
   com = ["sex", image, "-c "+sexdir+config,
          "-PARAMETERS_NAME "+sexdir+"default.param",
          "-DETECT_MINAREA 5", "-DETECT_THRESH " + str(thresh),
          "-ANALYSIS_THRESH " + str(thresh), "-PIXEL_SCALE %f" % (scale),
          "-SEEING_FWHM "+str(fwhm), "-CATALOG_NAME "+output,
          "-FILTER_NAME "+sexdir+"gauss_3.0_5x5.conv",
          "-STARNNW_NAME "+sexdir+"default.nnw",
          "-SATUR_LEVEL "+str(50000), "-VERBOSE_TYPE QUIET", "-CHECKIMAGE_NAME "+check_img]
   if gain is not None:
      com += ["-GAIN",str(gain)]
   if zmag is not None:
      com += ["-MAG_ZEROPOINT", str(zmag)]
   if sigma_map is not None:
      com += ["-WEIGHT_IMAGE",sigma_map,"-WEIGHT_TYPE MAP_WEIGHT"]
   com = string.join(com)
   #print com
   res = os.system(com)
   return res




#-------extract extentions-----------
def slice_fits(hdu=None,exten=None,output=None):
    data=hdu[exten].data
    header=hdu[exten].header
    header.update('exten',exten,'extension of the image')
    newhdu=pf.PrimaryHDU(data,header)
    newhdu.writeto(output)
    return 0



def dist(x):
    n=len(x)
    d=np.zeros((n,n))
    d[:,:]=-999.
    for i in range(0,n-1):
        for j in range(i+1,n):
            d[i,j]=np.abs(x[i]-x[j])
    d=d.flatten()
    d=d[d>=0]
    return(d)

def extract_ext(filename,ext):
    hdu=pf.open(filename)
    output=filename[0:-5]+'_exten_'+str(ext)+'.fits'
    t=slice_fits(hdu,ext,output)
    hdu.close()

def wcs2pix(ra,dec):
    """
    This only apply to MCCDTV with sispi mosaic image.
    y ~ ra
    x ~ dec
    y,x = wcs2pix(ra,dec)
    """
    if type(ra).__name__=='float':
        if ra > 180:
            ra=ra-360
        #y=ra*3600./0.27   #approximation
        #x=dec*3600./0.27
        x=3600*180./0.27/np.pi*np.sin(np.deg2rad(dec))
        y=3600*180./0.27/np.pi*np.cos(np.deg2rad(dec))*np.sin(np.deg2rad(ra))
    if type(ra).__name__=='ndarray':
        dra=np.argwhere(ra>180)
        if len(dra)>0:
            ra[dra]=ra[dra]-360
        #y=ra*3600./0.27   #approximation
        #x=dec*3600./0.27
        x=3600*180./0.27/np.pi*np.sin(np.deg2rad(dec)) #exact conversion
        y=3600*180./0.27/np.pi*np.cos(np.deg2rad(dec))*np.sin(np.deg2rad(ra))
    return y,x

#-----------------ccd match------------


def xy_matching(xa=None,ya=None,xb=None,yb=None,sep=None):
    n=len(xa)
    ind1=np.arange(n)
    ind2=np.arange(n)
    ind2[:]=-1
    for i in range(0,n):
        dd=np.sqrt((xb-xa[ind1[i]])**2+(yb-ya[ind1[i]])**2)
        id=np.where(dd < sep)
        if (len(id[0]) >= 1):
            ind2[i]=id[0][0]
    ok=np.where(ind2 != -1)
    ind2=ind2[ok]
    ind1=ind1[ok]    
    return ind1,ind2

def ccd_offset(CCD1,CCD2):
    
    if CCD1[0]=='s' or CCD1[0]=='S':
        idx1=int(CCD1[1:])
        x1_target = S[idx1][1]
        y1_target = S[idx1][2]
    else:
        idx1=int(CCD1[1:])
        x1_target = N[idx1][1]
        y1_target = N[idx1][2]
        
    if CCD2[0]=='s' or CCD2[0]=='S':
        idx2=int(CCD2[1:])
        x2_target = S[idx2][1]
        y2_target = S[idx2][2]
    else:
        idx2=int(CCD2[1:])
        x2_target = N[idx2][1]
        y2_target = N[idx2][2]
    xoffset=x2_target - x1_target
    yoffset=y2_target - y1_target
    xoffset=xoffset*1000./15. #convert to pixel unit
    yoffset=yoffset*1000./15.

    return -xoffset,yoffset


#--the coordinate should be in wcs converted to pixel coordinate-----

def ccd_match(CCD1=None,xa=None,ya=None,CCD2=None,xb=None,yb=None,xadd=None,yadd=None,sep=None):
    
    """
    ccd_match(CCD1=None,xa=None,ya=None,CCD2=None,xb=None,yb=None,sep=None)
    """
    xoffset,yoffset=ccd_offset(CCD1,CCD2)
    in1,in2=xy_matching(xa,ya,xb-xoffset-xadd,yb-yoffset-yadd,sep=sep)
    return in1,in2





def match_analysis(xa=None,ya=None,xb=None,yb=None,ina=None,inb=None):
    xdff=xa[ina]-xb[inb]
    ydff=ya[ina]-yb[inb]

    fig=pl.figure(figsize=(9,8),dpi=100)
    ax=fig.add_subplot(2,2,1)
    pl.plot(xa,ya,'bo')
    pl.plot(xa[ina],ya[ina],'r.')
    pl.title('image 1: red dot is cross-matched')
    ax=fig.add_subplot(2,2,2)
    pl.plot(xb,yb,'bo')
    pl.plot(xb[inb],yb[inb],'r.')
    pl.title('image 2: red dot is cross-matched')
    ax=fig.add_subplot(2,2,3)
    xpeak=pl.hist(xdff,bins=80,range=(-0.5,0.5))
    xpeak=max(xpeak[0])
    pl.xlim(-0.3,0.3)
    pl.ylim(0,1.5*xpeak)
    pl.xlabel('x (dec) difference (pixels)')
    pl.text(0.1,0.9,'difference: '+str(round(robust_mean(xdff),5))+'+/-'+str(round(robust_std(xdff),5)),transform = ax.transAxes)
    ax=fig.add_subplot(2,2,4)
    ypeak=pl.hist(ydff,bins=80,range=(-0.5,0.5))
    ypeak=max(ypeak[0])
    pl.xlim(-0.3,0.3)
    pl.ylim(0,1.5*ypeak)
    pl.xlabel('y (ra) difference (pixels)')
    pl.text(0.1,0.9,'difference: '+str(round(robust_mean(ydff),5))+'+/-'+str(round(robust_std(ydff),5)),transform = ax.transAxes)   
    return 0


def ccd_match_analysis(CCD1=None,xa=None,ya=None,ina=None,CCD2=None,xb=None,yb=None,inb=None):
    dxa=dist(xa[ina])
    dxb=dist(xb[inb])
    dya=dist(ya[ina])
    dyb=dist(yb[inb])
    xtan=(dxb-dxa)/(dxb)
    ytan=(dyb-dya)/(dyb)
    fig=pl.figure(figsize=(14,14))
    ax=fig.add_subplot(2,2,1)
    pl.plot(xa,ya,'bo')
    pl.plot(xa[ina],ya[ina],'r.')
    pl.title(CCD1+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,2)
    pl.plot(xb,yb,'bo')
    pl.plot(xb[inb],yb[inb],'r.')
    pl.title(CCD2+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,3)
    xlarge=(dxa > 500)*(dxb>500)
    ylarge=(dya>500)*(dyb> 500)
    dxa=dxa[xlarge]
    dxb=dxb[xlarge]
    dya=dya[ylarge]
    dyb=dyb[ylarge]
    xtan=xtan[xlarge]
    ytan=ytan[ylarge]
    xcept,xslope,xcept_err,xslope_err,xchi2 = linefit(dxb,xtan)
    ycept,yslope,ycept_err,yslope_err,ychi2 = linefit(dyb,ytan)
    pl.plot(dxb,xtan,'bo')
    pl.plot(np.array([min(dxb)-200,max(dxb)+200]),np.array([min(dxb)-200,max(dxb)+200])*xslope+xcept,'r-')
    pl.text(0.1,0.9,'slope: '+str(round(xslope,5)),transform = ax.transAxes)
    pl.text(0.1,0.85,'intercept: '+str(round(xcept,5)),transform = ax.transAxes)
    pl.title('x(dec) direction')
    pl.xlabel('separations on '+CCD2)
    pl.ylabel('(dxb-dxa)/dxb')
    ax=fig.add_subplot(2,2,4)
    pl.plot(dyb,ytan,'bo')
    pl.plot(np.array([min(dyb)-200,max(dyb)+200]),np.array([min(dyb)-200,max(dyb)+200])*yslope+ycept,'r-')
    pl.text(0.1,0.9,'slope: '+str(round(yslope,5)),transform = ax.transAxes)
    pl.text(0.1,0.85,'intercept: '+str(round(ycept,5)),transform = ax.transAxes)
    pl.title('y(ra) direction')
    pl.xlabel('separations on '+CCD2)
    pl.ylabel('(dyb-dya)/dyb')



def ccd_match_offset_bak(CCD1=None,xa=None,ya=None,ina=None,CCD2=None,xb=None,yb=None,inb=None,xadd=None,yadd=None,crit_f=None):
    if crit_f == None:
        crit_f=0.
    dxa=dist(xa[ina])
    dxb=dist(xb[inb])
    dya=dist(ya[ina])
    dyb=dist(yb[inb])
    xoffset,yoffset=ccd_offset(CCD1,CCD2)    
    xtan=(dxb-dxa)/(dxa)
    ytan=(dyb-dya)/(dya)
    fig=pl.figure(figsize=(8,5),dpi=100)
    """
    ax=fig.add_subplot(2,2,1)
    pl.plot(xa,ya,'bo')
    if len(inb) > 1:
        pl.plot(xb[inb]-xoffset-xadd,yb[inb]-yoffset-yadd,'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD1+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,2)
    pl.plot(xb-xoffset-xadd,yb-yoffset-yadd,'bo')
    if len(ina) > 1:
        pl.plot(xa[ina],ya[ina],'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD2+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,3)
    """
    ax=fig.add_subplot(1,2,1)
    xlarge=(dxa > 300)*(dxb>300)
    ylarge=(dya>300)*(dyb> 300)
    dxa=dxa[xlarge]
    dxb=dxb[xlarge]
    dya=dya[ylarge]
    dyb=dyb[ylarge]
    xtan=xtan[xlarge]*200000/15.
    ytan=ytan[ylarge]*200000/15.
    xpeak=pl.hist(xtan,bins=1000)
    xpeak=max(xpeak[0])
    mean_xtan,stdm_xtan,ks_x,ks_p_x=mode_gauss(xtan,binsize=1,range=(-150,150),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_xtan,0,xpeak,'r')
    pl.ylim(0,1.5*xpeak)
    pl.text(0.1,0.9,'x(dec) direction',transform = ax.transAxes)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_xtan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_xtan,8)),transform = ax.transAxes)
    #pl.text(0.1,0.78,'KS normality test p-value: '+str(round(ks_p_x,8)),transform = ax.transAxes)
    pl.xlabel('offset of '+CCD2+' w.r.t. '+CCD1+'(pixels)')
    pl.xlim(-100,100)
    ax=fig.add_subplot(1,2,2)
    ypeak=pl.hist(ytan,bins=1000)
    ypeak=max(ypeak[0])
    mean_ytan,stdm_ytan,ks_y,ks_p_y=mode_gauss(ytan,binsize=1,range=(-150,150),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_ytan,0,ypeak,'r')
    pl.ylim(0,1.5*ypeak)
    pl.text(0.1,0.9,'y(ra) direction',transform = ax.transAxes)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_ytan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_ytan,8)),transform = ax.transAxes)
    #pl.text(0.1,0.78,'KS normality test p-value: '+str(round(ks_p_y,8)),transform = ax.transAxes)
    pl.xlabel('offset of '+CCD2+' w.r.t. '+CCD1+' (pixels)')
    pl.xlim(-100,100)
    return mean_xtan,stdm_xtan,mean_ytan,stdm_ytan



def ccd_match_offset(CCD1=None,xa=None,ya=None,ina=None,CCD2=None,xb=None,yb=None,inb=None,xadd=None,yadd=None,crit_f=None):
    if crit_f == None:
        crit_f=0.
    dxa=dist(xa[ina])
    dxb=dist(xb[inb])
    dya=dist(ya[ina])
    dyb=dist(yb[inb])
    dla=np.sqrt(dxa**2+dya**2)
    dlb=np.sqrt(dxb**2+dyb**2)
    xoffset,yoffset=ccd_offset(CCD1,CCD2)    
    ltan=(dlb-dla)/dla
    fig=pl.figure(figsize=(11,11),dpi=100)
    ax=fig.add_subplot(2,2,1)
    pl.plot(xa,ya,'bo')
    if len(inb) > 1:
        pl.plot(xb[inb]-xoffset-xadd,yb[inb]-yoffset-yadd,'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD1+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,2)
    pl.plot(xb-xoffset-xadd,yb-yoffset-yadd,'bo')
    if len(ina) > 1:
        pl.plot(xa[ina],ya[ina],'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD2+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,3)
    large=(dla > 300)*(dlb > 300)
    ltan=ltan[large]*200000/15.
    lpeak=pl.hist(ltan,bins=1000)
    lpeak=max(lpeak[0])
    mean_ltan,stdm_ltan,ks_l,ks_p_l=mode_gauss(ltan,binsize=1,range=(-150,150),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_ltan,0,lpeak,'r')
    pl.ylim(0,1.5*lpeak)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_ltan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_ltan,8)),transform = ax.transAxes)
    pl.xlabel('offset of '+CCD2+' w.r.t. '+CCD1+'(pixels)')
    pl.xlim(-100,100)
    return mean_ltan,stdm_ltan



def ccd_match_offset_for_tilt_bak(CCD1=None,xa=None,ya=None,ina=None,CCD2=None,xb=None,yb=None,inb=None,xadd=None,yadd=None,crit_f=None,dd=None):
    if crit_f == None:
        crit_f=0.
    dxa=dist(xa[ina])
    dxb=dist(xb[inb])
    dya=dist(ya[ina])
    dyb=dist(yb[inb])
    
    xoffset,yoffset=ccd_offset(CCD1,CCD2)    
    xtan=(dxb-dxa)/(dxb)
    ytan=(dyb-dya)/(dyb)
    fig=pl.figure(figsize=(8,5),dpi=100)
    """
    ax=fig.add_subplot(2,2,1)
    pl.plot(xa,ya,'bo')
    if len(inb) > 1:
        pl.plot(xb[inb]-xoffset-xadd,yb[inb]-yoffset-yadd,'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD1+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,2)
    pl.plot(xb-xoffset-xadd,yb-yoffset-yadd,'bo')
    if len(ina) > 1:
        pl.plot(xa[ina],ya[ina],'r.')
    pl.xlim(min(xa)-200,max(xa)+200)
    pl.ylim(min(ya)-200,max(ya)+200)
    pl.xlabel('x (pixels)')
    pl.xlabel('y (pixels)')
    pl.title(CCD2+': red dot is cross-matched')
    ax=fig.add_subplot(2,2,3)
    """
    ax=fig.add_subplot(1,2,1)
    xlarge=(dxa > 300)*(dxb>300)
    ylarge=(dya>300)*(dyb> 300)
    dxa=dxa[xlarge]
    dxb=dxb[xlarge]
    dya=dya[ylarge]
    dyb=dyb[ylarge]
    xtan=xtan[xlarge]*200000/15/dd
    ytan=ytan[ylarge]*200000/15/dd
    xpeak=pl.hist(xtan,bins=1000)
    xpeak=max(xpeak[0])
    mean_xtan,stdm_xtan,ks_x,ks_p_x=mode_gauss(xtan,binsize=0.0001,range=(-0.1,0.1),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_xtan,0,xpeak,'r')
    pl.ylim(0,1.5*xpeak)
    pl.text(0.1,0.9,'x(dec) direction',transform = ax.transAxes)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_xtan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_xtan,8)),transform = ax.transAxes)
    pl.xlabel('Tangent of the tilt angle')
    pl.xlim(-0.100,0.100)
    ax=fig.add_subplot(1,2,2)
    ypeak=pl.hist(ytan,bins=1000)
    ypeak=max(ypeak[0])
    mean_ytan,stdm_ytan,ks_y,ks_p_y=mode_gauss(ytan,binsize=0.00011,range=(-0.1,0.1),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_ytan,0,ypeak,'r')
    pl.ylim(0,1.5*ypeak)
    pl.text(0.1,0.9,'y(ra) direction',transform = ax.transAxes)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_ytan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_ytan,8)),transform = ax.transAxes)
    pl.xlabel('Tangent of the tilt angle')
    pl.xlim(-0.1,0.100)
    return mean_xtan,stdm_xtan,mean_ytan,stdm_ytan



def ccd_match_offset_for_tilt(CCD1=None,xa=None,ya=None,ina=None,CCD2=None,xb=None,yb=None,inb=None,xadd=None,yadd=None,crit_f=None,dd=None):
    if crit_f == None:
        crit_f=0.
    dxa=dist(xa[ina])
    dxb=dist(xb[inb])
    dya=dist(ya[ina])
    dyb=dist(yb[inb])
    dla=np.sqrt(dxa**2+dya**2)
    dlb=np.sqrt(dxb**2+dyb**2)
   
    xoffset,yoffset=ccd_offset(CCD1,CCD2)    
    ltan=(dlb-dla)/dlb
    fig=pl.figure(figsize=(8,8),dpi=100)
    ax=fig.add_subplot(1,1,1)
    large=(dla > 300)*(dlb > 300)
    ltan=ltan[large]*200000/15./dd
    lpeak=pl.hist(ltan,bins=1000)
    lpeak=max(lpeak[0])
    mean_ltan,stdm_ltan,ks_x,ks_p_x=mode_gauss(ltan,binsize=0.0001,range=(-0.1,0.1),crit_f=crit_f)
    pl.hlines(crit_f,-100,100,'r')
    pl.vlines(mean_ltan,0,lpeak,'r')
    pl.ylim(0,1.5*lpeak)
    pl.text(0.1,0.85,'Mean: '+str(round(mean_ltan,8)),transform = ax.transAxes)
    pl.text(0.1,0.78,'Std to mean: '+str(round(stdm_ltan,8)),transform = ax.transAxes)
    pl.xlabel('Tangent of the tilt angle')
    pl.xlim(-0.100,0.100)
   
    return mean_ltan,stdm_ltan








def ccd2file(CCD):
    if CCD=='s1':
        fileNo=0
    if CCD=='s2':
        fileNo=1
    if CCD=='s3':
        fileNo=2
    if CCD=='s4':
        fileNo=3
    if CCD=='s5':
        fileNo=4
    if CCD=='s6':
        fileNo=5
    if CCD=='s7':
        fileNo=6
    if CCD=='n7':
        fileNo=7
    if CCD=='n6':
        fileNo=8
    if CCD=='n5':
        fileNo=9
    if CCD=='n4':
        fileNo=10
    if CCD=='n2':
        fileNo=11
    if CCD=='n1':
        fileNo=12
    if CCD=='s9':
        fileNo=13
    if CCD=='s10':
        fileNo=14
    if CCD=='s11':
        fileNo=15
    if CCD=='s12':
        fileNo=16
    if CCD=='s13':
        fileNo=17
    return fileNo


def ccd_flux_threshold(cat=None,CCD=None,fluxth=None):
    b0=pf.getdata(cat[ccd2file(CCD)])
    f0=b0.field('FLUX_BEST')
    if fluxth:
        ok0=f0>fluxth
    else:
        ok0=f0>np.mean(f0)
    ra0=b0.field('X_WORLD')[ok0]
    dec0=b0.field('Y_WORLD')[ok0]
    y0,x0=wcs2pix(ra0,dec0)
    pl.plot(x0,y0,'bo')


def offset(CCD1=None,CCD2=None,cat=None,xadd=None,yadd=None,sep=None,crit_f=None):
    
    b0=pf.getdata(cat[ccd2file(CCD1)])
    b1=pf.getdata(cat[ccd2file(CCD2)])

    f0=b0.field('FLUX_BEST')
    f1=b1.field('FLUX_BEST')

    #ok0=f0>np.mean(f0)
    #ok1=f1>np.mean(f1)
    ok0=f0>120000
    ok1=f1>120000
    
    ra0=b0.field('X_WORLD')[ok0]
    dec0=b0.field('Y_WORLD')[ok0]
    ra1=b1.field('X_WORLD')[ok1]
    dec1=b1.field('Y_WORLD')[ok1]

    y0,x0=wcs2pix(ra0,dec0)
    y1,x1=wcs2pix(ra1,dec1)

    in1,in2=ccd_match(CCD1=CCD1,xa=x0,ya=y0,CCD2=CCD2,xb=x1,yb=y1,xadd=xadd,yadd=yadd,sep=sep)
    #mean_xtan,stdm_xtan,mean_ytan,stdm_ytan=ccd_match_offset(CCD1=CCD1,xa=x0,ya=y0,CCD2=CCD2,xb=x1,yb=y1,ina=in1,inb=in2,xadd=xadd,yadd=yadd,crit_f=crit_f)
    #return mean_xtan,stdm_xtan,mean_ytan,stdm_ytan
    mean_ltan,stdm_ltan=ccd_match_offset(CCD1=CCD1,xa=x0,ya=y0,CCD2=CCD2,xb=x1,yb=y1,ina=in1,inb=in2,xadd=xadd,yadd=yadd,crit_f=crit_f)
    return mean_ltan,stdm_ltan



def ccd_match_check(cat=None,CCD1=None,CCD2=None):
    b0=pf.getdata(cat[ccd2file(CCD1)])
    b1=pf.getdata(cat[ccd2file(CCD2)])
    f0=b0.field('FLUX_BEST')
    f1=b1.field('FLUX_BEST')
    #ok0=f0>np.mean(f0)
    #ok1=f1>np.mean(f1)
    ok0=f0>120000
    ok1=f1>120000
    
    ra0=b0.field('X_WORLD')[ok0]
    dec0=b0.field('Y_WORLD')[ok0]
    ra1=b1.field('X_WORLD')[ok1]
    dec1=b1.field('Y_WORLD')[ok1]
    y0,x0=wcs2pix(ra0,dec0)
    y1,x1=wcs2pix(ra1,dec1)
    pl.subplot(2,2,1)
    pl.plot(x0,y0,'bo')
    pl.title(CCD1)
    pl.subplot(2,2,2)
    pl.plot(x1,y1,'bo')
    pl.title(CCD2)
    pl.subplot(2,2,3)
    xoffset,yoffset=ccd_offset(CCD1,CCD2)
    pl.plot(x0,y0,'bo')
    pl.plot(x1-xoffset,y1-yoffset,'r.')
    pl.title(CCD2 +' moved to '+CCD1 )









def ccd_match_optimal(CCD1=None,xa=None,ya=None,CCD2=None,xb=None,yb=None,sep=None):
    
    """
    ccd_match(CCD1=None,xa=None,ya=None,CCD2=None,xb=None,yb=None,sep=None)
    """
    xoffset,yoffset=ccd_offset(CCD1,CCD2)
    in1,in2=xy_matching(xa,ya,xb-xoffset,yb-yoffset,sep=sep)
    nmatch=len(in1)
    for i in range(3000):
        print i
        xoffset=xoffset+np.random.randint(-80,80)
        yoffset=yoffset+np.random.randint(-80,80)
        ind1,ind2=xy_matching(xa,ya,xb-xoffset,yb-yoffset,sep=sep)    
        nm=len(ind1)
        if nm > nmatch:
            in1=ind1
            in2=ind2
            nmatch=nm
    return in1,in2

def ccd_tilt(CCD=None,cat=None,fileNoa=None,fileNob=None,xadd=None,yadd=None,sep=None,crit_f=None,dd=None):
    filediff=abs(fileNob-fileNoa)
    b0=pf.getdata(cat[fileNoa])
    b1=pf.getdata(cat[fileNob])

    xtan=np.zeros(0)
    ytan=np.zeros(0)

    f0=b0.field('FLUX_BEST')
    f1=b1.field('FLUX_BEST')

    #ok0=f0>np.mean(f0)
    #ok1=f1>np.mean(f1)
    ok0=f0>120000
    ok1=f1>120000
    
    ra0=b0.field('X_WORLD')[ok0]
    dec0=b0.field('Y_WORLD')[ok0]
    ra1=b1.field('X_WORLD')[ok1]
    dec1=b1.field('Y_WORLD')[ok1]
    
    ya,xa=wcs2pix(ra0,dec0)
    yb,xb=wcs2pix(ra1,dec1)
    
    ina,inb=ccd_match(CCD1=CCD,xa=xa,ya=ya,CCD2=CCD,xb=xb,yb=yb,xadd=xadd,yadd=yadd,sep=sep)
    mean_ltan,stdm_ltan=ccd_match_offset_for_tilt(CCD1=CCD,xa=xa,ya=ya,CCD2=CCD,xb=xb,yb=yb,ina=ina,inb=inb,xadd=xadd,yadd=yadd,crit_f=crit_f,dd=dd)
   
    
    #mean_xtan,stdm_xtan,mean_ytan,stdm_ytan=ccd_match_offset_for_tilt(CCD1=CCD,xa=xa,ya=ya,CCD2=CCD,xb=xb,yb=yb,ina=ina,inb=inb,xadd=xadd,yadd=yadd,crit_f=crit_f,dd=dd)
    #return mean_xtan,stdm_xtan,mean_ytan,stdm_ytan


  







