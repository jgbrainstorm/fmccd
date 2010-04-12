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


#-----Robust Mean--------------
def robust_mean(x):
    y = x.flatten()
    n = len(y)
    y.sort()
    ind_qt1 = round((n+1)/4.)
    ind_qt3 = round((n+1)*3/4.)
    IQR = y[ind_qt3]- y[ind_qt1]
    lowFense = y[ind_qt1] - 1.5*IQR
    highFense = y[ind_qt3] + 1.5*IQR
    ok = (y>lowFense)*(y<highFense)
    yy=y[ok]
    return yy.mean(dtype='double')


#-------Robust Standard Deviation---

def robust_std(x):
    y = x.flatten()
    n = len(y)
    y.sort()
    ind_qt1 = round((n+1)/4.)
    ind_qt3 = round((n+1)*3/4.)
    IQR = y[ind_qt3]- y[ind_qt1]
    lowFense = y[ind_qt1] - 1.5*IQR
    highFense = y[ind_qt3] + 1.5*IQR
    ok = (y>lowFense)*(y<highFense)
    yy=y[ok]
    return yy.std(dtype='double')

#-------Robust variance---

def robust_var(x):
    y = x.flatten()
    n = len(y)
    y.sort()
    ind_qt1 = round((n+1)/4.)
    ind_qt3 = round((n+1)*3/4.)
    IQR = y[ind_qt3]- y[ind_qt1]
    lowFense = y[ind_qt1] - 1.5*IQR
    highFense = y[ind_qt3] + 1.5*IQR
    ok = (y>lowFense)*(y<highFense)
    yy=y[ok]
    return yy.var(dtype='double')




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
    NChannel = len(medianHDU)
    Nfile = len(imagName)
    totalIMG = np.zeros((Nfile,medianHDU[1].data.shape[0],medianHDU[1].data.shape[1]))
    for i in range(1,NChannel):     # i runs for channel
        for j in range(0,Nfile):    # j runs for file
            imagHDU = pf.open(imagName[j])          
            totalIMG[j,:,:] = imagHDU[i].data
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

def Img_sub(imageName,biasName):
    imageHDU=pf.open(imageName,mode='update')
    biasHDU=pf.open(biasName)
    NChannel = len(imageHDU)
    for i in range(1,NChannel):
        imageHDU[i].data = imageHDU[i].data - biasHDU[i].data
   # HDU = scaleHDU(medianHDU) """ scale the image"""
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

"""

#-----------------------------------------------------
#Calculate the gain of ccd readouts of a given Channel.
#-----------------------------------------------------

def gain_channel(NameFits,NameBias,Channel,shift=None,plot=None,figdir=None):

    ymin=150
    ymax=350
    xmin=500 
    xmax=800
    
    left = np.mod(Channel,2)
    

    NFile = len(NameFits)
    num = round((NFile-1)/2.)
     
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    
    if shift == 1:
        yshift = np.random.random_integers(0,500,1)
        xshift = np.random.random_integers(0,3000,1)
        xmin = xmin + xshift
        xmax = xmax + xshift
        ymin = ymin + yshift
        ymax = ymax + yshift

   # bias,biashdr = readCCDFits(NameBias,Channel)
   # bias = bias[xmin:xmax,ymin:ymax]

    for i in range(0,num):
        print i
        bias,biashdr = readCCDFits(NameBias[0],Channel)
        bias = bias[xmin:xmax,ymin:ymax]
        ba,hdra = readCCDFits(NameFits[i*2],Channel)
        ba = ba[xmin:xmax,ymin:ymax]
        ba = ba - bias
        bb,hdrb = readCCDFits(NameFits[i*2+1],Channel)
        bb = bb[xmin:xmax,ymin:ymax]
        bb = bb - bias
        uni = np.unique(ba)
        add_b = ba + bb
        diff_b= ba - bb
        mean_b[i] = robust_mean(add_b)/2.
        var_b[i] = robust_var(diff_b)/2.

        if len(uni) < 10:
            if np.max(ba) > 20000:
               return 'Saturated'
            else:
               return 'N/A'
        else:

            ok = (mean_b > 0)*(mean_b <3500)

    if len(mean_b[ok]) > 2:
        (slope,intercept) = np.polyfit(mean_b[ok],var_b[ok],1)
        gain = slope;
    else:
        return 'N/A'
    gain=1
    
    if plot == 1:

      #  figdir = '/data/MCCDTV_Testing_Results/Jun-8-2009/'
        pl.plot(mean_b,var_b,'bo',mean_b,slope*mean_b+intercept,'-')
        pl.xlabel('Mean Signal')
        pl.ylabel('Variance')
        pl.title('Photon Transfer Curve For Channel:'+str(Channel))
        ax = pl.axes()
        pl.text(0.1,.85,'Gain:'+str(gain)+'(e-/ADU)',transform = ax.transAxes)
        pl.savefig(figdir+'gain_'+hdra[17]+str(left)+'.png')
        pl.close()
    return gain

"""


def linearity(NameFits,NameBias,Channel,shift=None,left=None):

    if left == None or left == 1:
        ymin=150
        ymax=350
        xmin=200 #lower
        xmax=500
        #xmin=2000 #middle
        #xmax=2500
    else:
        ymin=1300
        ymax=1750
        xmin=200
        xmax=500
        #xmin=2000 #middle
        #xmax=2500
    #xmin=3600 #upper
    #xmax=4000
    if shift == 1:
        yshift = np.random.random_integers(0,500,1)
        xshift = np.random.random_integers(0,3000,1)
        xmin = xmin + xshift
        xmax = xmax + xshift
        ymin = ymin + yshift
        ymax = ymax + yshift
    NFile = len(NameFits)
    num = round((NFile-1)/2.)
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    exptime=np.zeros(num)
    for i in range(0,num):
        bias,biashdr = readCCDFits(NameBias[0],Channel)
        bias = bias[xmin:xmax,ymin:ymax]
        ba,hdra = readCCDFits(NameFits[i*2],Channel)
        ba = ba[xmin:xmax,ymin:ymax]
        ba = ba - bias
        bb,hdrb = readCCDFits(NameFits[i*2+1],Channel)
        bb = bb[xmin:xmax,ymin:ymax]
        bb = bb - bias
        uni = np.unique(ba)
        add_b = ba + bb
        diff_b= ba - bb
        mean_b[i] = robust_mean(add_b)/2.
        var_b[i] = robust_var(diff_b)/2.
        exptime[i]=pf.open(NameFits[i*2])[0].header['exptime']        
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
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Bias subtracted mean counts (ADU)')
    pl.title('Linearity plot for Channel: '+str(Channel))
    ax=fig.add_subplot(2,2,2)
    pl.plot(exptime,(mean_b-(tb*exptime+ta))/(tb*exptime+ta),'bo')
    pl.hold(True)
    pl.hlines(0.01,0,300,colors='r',linestyles='dashed')
    pl.hlines(-0.01,0,300,colors='r',linestyles='dashed')
    pl.ylim(-0.1,0.1)
    pl.xlabel('Exposure time (sec)')
    pl.ylabel('Relative deviation from the fitted line')    
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

def noise_channel(NameFits,Channel,plot=None,shift=None,figdir=None):

    left = np.mod(Channel,2)
    if left == 1:
        ncolmin=15
      	ncolmax=50
      	nrowmin=1000
      	nrowmax=2000
    else:   
        ncolmin=1025
      	ncolmax=1074
      	nrowmin=1000
      	nrowmax=2000
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
        pl.xlabel('Subtracted Pixel Values in Overscan (ADU)')
        pl.title('Readout Noise for Channel:'+str(Channel))
        pl.legend(('Mean:'+str(robust_mean(nois)),'Sd:'+str(robust_std(nois))))
        pl.savefig(figdir+'noise_'+hdrn[17]+str(left)+'.png')
     #  pl.show()
        pl.close()
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

    idd = (ss > 10000)*(ss < 65000)
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



#-----move the xy stage


#---auto xtalk coef---------
def xcoeff(imgNumber=None,source=None,victim=None,winSg=None,winBg=None,NamePng=None):
      
    colmin = winSg[0]
    colmax = winSg[1]
    rowmin = winSg[2]
    rowmax = winSg[3]
   
    colminBg = winBg[0]    # for background substraction
    colmaxBg = winBg[1]
    rowminBg = winBg[2]
    rowmaxBg = winBg[3]
    
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

    idd = (ss > 10000)*(ss < 65000)
    ss=ss[idd]
    vv=vv[idd]
    vverr = np.sqrt(np.abs(vv))

    (a,b,SEa,SEb,chi2) = linfit(ss,vv,vverr)
    """
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
    pl.plot(np.array([10000,65000]),np.array([10000,65000])*b+a,'r-')
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
    """
    return(b)
