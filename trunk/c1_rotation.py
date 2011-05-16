#! /usr/bin/env python
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *

ext=np.array([8,19,20,3,42,37])

catdir='/data/jiangang/C1-projector-rotations/catalog/'

for k in ext:
    CatFits=gl.glob(catdir+'*_exten_'+str(k)+'_*.fits')
    CatFits.sort()
    Nfits=len(CatFits)
    for i in range(Nfits):
        x0=pf.getdata(CatFits[0]).field('x_image')
        y0=pf.getdata(CatFits[0]).field('y_image')
        flux=pf.getdata(CatFits[0]).field('flux_best')
        ok=flux>np.mean(flux)
        x0=x0[ok]
        y0=y0[ok]
    Mxdiff=[]
    Mydiff=[]
    SDxdiff=[]
    SDydiff=[]
    for j in range(1,len(CatFits)):
        x1=pf.getdata(CatFits[j]).field('x_image')
        y1=pf.getdata(CatFits[j]).field('y_image')
        flux=pf.getdata(CatFits[j]).field('flux_best')
        ok=flux>np.mean(flux)
        x1=x1[ok]
        y1=y1[ok]
        i0,i1=xy_matching(xa=x0,ya=y0,xb=x1,yb=y1,sep=60)
        Mydiff.append(np.mean(y1[i1]-y0[i0]))
        Mxdiff.append(np.mean(x1[i1]-x0[i0]))
        SDydiff.append(np.std(y1[i1]-y0[i0]))
        SDxdiff.append(np.std(x1[i1]-x0[i0]))
    Mydiff=np.array(Mydiff)
    Mxdiff=np.array(Mxdiff)
    SDydiff=np.array(SDydiff)
    SDxdiff=np.array(SDxdiff)
    angle=np.array([131,45,90])
    aax,bx,SEax,SEbx,chi2x=linfit(angle,Mxdiff,SDxdiff)
    aay,by,SEay,SEby,chi2y=linfit(angle,Mydiff,SDxdiff)
    fig=pl.figure(figsize=(15,8))
    ax=fig.add_subplot(1,2,1)
    pl.errorbar(angle,Mydiff,yerr=SDydiff,fmt='bo')
    #pl.plot(angle,by*angle+aay,'r-')
    pl.xlabel('Rotation position (degree)')
    pl.ylabel('image shift w.r.t. 0 degree in y direction (pixels)')
    #pl.text(0.2,0.85,'slope: '+str(round(by,3))+r'$\pm$'+str(round(SEby,3)),transform = ax.transAxes)
    #pl.text(0.2,0.8,'Itcpt: '+str(round(aay,3))+r'$\pm$'+str(round(SEay,3)),transform = ax.transAxes)
    pl.title('Extension: '+str(k))
    pl.ylim(-60,30)
    ax=fig.add_subplot(1,2,2)
    pl.errorbar(angle,Mxdiff,yerr=SDxdiff,fmt='bo')
    #pl.plot(angle,bx*angle+aax,'r-')
    pl.xlabel('Rotation position (degree)')
    pl.ylabel('image shift w.r.t. 0 degree in x direction (pixels)')
    #pl.text(0.2,0.85,'slope: '+str(round(bx,3))+r'$\pm$'+str(round(SEbx,3)),transform = ax.transAxes)
    #pl.text(0.2,0.8,'Itcpt: '+str(round(aax,3))+r'$\pm$'+str(round(SEax,3)),transform = ax.transAxes)
    pl.ylim(-60,30)
    pl.savefig('c1_rotation_ext_'+str(k)+'.png')
    pl.close()
