#! /usr/bin/env python
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *


def lin(NameFits,NameBias,Channel,rowshift=None,left=None):

    if left == 1:
        colmin=300
        colmax=800
    else:
        colmin=1300
        colmax=1800
    rowmin=100+rowshift
    rowmax=200+rowshift
    #detector = pf.open(NameBias)[Channel].header['DETSER']
    detector = pf.open(NameBias)[Channel].header['DETPOS']
    if detector[-1]=='N':
        rowmin=3946-rowshift
        rowmax=4046-rowshift
    if detector[0]=='F':
        rowmin=100+rowshift
        rowmax=200+rowshift
    NFile = len(NameFits)
    num = round((NFile-1)/2.)
    mean_b = np.zeros(num)
    var_b = np.zeros(num)
    exptime=np.zeros(num)
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
        exptime[i]=pf.open(NameFits[i*2])[0].header['expreq']        
        #exptime[i]=0
        ok = (mean_b > 0)*(mean_b <20000)*(var_b < 8000)          
        if len(mean_b[ok]) > 2:
            (a,b,SEa,SEb,R2) = linefit(mean_b[ok],var_b[ok])
            gain = b
        else:
            gain=999
            a=0
            b=0
            SEb=999
    diff=(var_b-(b*mean_b+a))/(b*mean_b+a)
    uu=mean_b[(abs(diff) > 0.1)*(mean_b > 15000)]
    if uu.any() == True:
        fwid=np.argwhere(mean_b==min(uu))
        fwid=fwid-1
        fw=mean_b[fwid]
    else:
        fw=999
        fwid=0
    return gain,fw[0][0]



dir=os.getcwd()+'/'

NameFits=gl.glob(dir+'/*.fits*')
NameBias=dir+'/bias/median.fits'
NameFits.sort()

hdu=pf.open(NameBias)
Channel=int(sys.argv[1])
left=int(sys.argv[2])
rowshift=np.arange(0,4000,500)

fullwell=[]
gain=[]

for i in rowshift:
    g,fw=lin(NameFits,NameBias,Channel,i,left=left)
    gain.append(g)
    fullwell.append(fw)
    print g, fw
    
fullwell=np.array(fullwell)
gain=np.array(gain)
hdr=pf.getheader(NameBias,Channel)
detname=hdr['detpos']

pl.figure(figsize=(14,7))
pl.subplot(1,2,1)
pl.plot(rowshift,fullwell,'bo')
pl.xlabel('row position')
pl.ylabel('full well capacity(ADU)')
pl.ylim(min(fullwell)-5000,max(fullwell)+10000)
pl.xlim(-100,4000)
if left==1:
    pl.title(detname+': left')
else:
    pl.title(detname+': right')

pl.subplot(1,2,2)
pl.plot(rowshift,fullwell/gain,'bo')
pl.xlabel('row position')
pl.ylabel('full well capacity (e-)')
pl.xlim(-100,4000)
pl.ylim(min(fullwell)-5000,max(fullwell/gain)+10000)
if left==1:
    pl.title(detname+': left')
else:
    pl.title(detname+': right')

pl.show()
    
    

