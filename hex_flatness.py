#! /usr/bin/env python
import sys
sys.path.append('/home/jghao/fmccd')
from fermiMCCD import *
ext=np.array([2,3,5,41,42,38,39,8,19,20,21])



#catdir='/data/10Jan2011_0deg/hexpodmove/catalog/'
catdir='/data/jiangang/zenith/hexpod_move/catalog/'

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
    for j in range(1,7):
        x1=pf.getdata(CatFits[j]).field('x_image')
        y1=pf.getdata(CatFits[j]).field('y_image')
        i0,i1=xy_matching(xa=x0,ya=y0,xb=x1,yb=y1,sep=20)
        Mydiff.append(np.mean(y1[i1]-y0[i0]))
        Mxdiff.append(np.mean(x1[i1]-x0[i0]))
        SDydiff.append(np.std(y1[i1]-y0[i0])/np.sqrt(len(i1)))
        SDxdiff.append(np.std(x1[i1]-x0[i0])/np.sqrt(len(i1)))  
    Mydiff=np.array(Mydiff)
    Mxdiff=np.array(Mxdiff)
    SDydiff=np.array(SDydiff)
    SDxdiff=np.array(SDxdiff)
    xshift=np.arange(-3000,3000,1000)
    aax,bx,SEax,SEbx,chi2x=linfit(xshift,Mxdiff,SDxdiff)
    aay,by,SEay,SEby,chi2y=linfit(xshift,Mydiff,SDxdiff)
    fig=pl.figure(figsize=(15,8))
    ax=fig.add_subplot(1,2,1)
    pl.errorbar(xshift,Mydiff,yerr=SDydiff,fmt='bo')
    pl.plot(xshift,by*xshift+aay,'r-')
    pl.xlabel('Hexpod shift in z direction (micron)')
    pl.ylabel('image shift in y direction (pixels)')
    pl.text(0.2,0.85,'slope: '+str(round(by,5))+r'$\pm$'+str(round(SEby,5)),transform = ax.transAxes)
    pl.text(0.2,0.8,'Itcpt: '+str(round(aay,5))+r'$\pm$'+str(round(SEay,5)),transform = ax.transAxes)
    pl.text(0.2,0.75,'Chi2: '+str(round(chi2y,5)),transform = ax.transAxes)
    pl.title('Extension: '+str(k))
    pl.ylim(-30,30)
    pl.xlim(-3100,3100)
    ax=fig.add_subplot(1,2,2)
    pl.errorbar(xshift,Mxdiff,yerr=SDxdiff,fmt='bo')
    pl.plot(xshift,bx*xshift+aax,'r-')
    pl.xlabel('Hexpod shift in z direction (micron)')
    pl.ylabel('image shift in x direction (pixels)')
    pl.text(0.2,0.85,'slope: '+str(round(bx,5))+r'$\pm$'+str(round(SEbx,5)),transform = ax.transAxes)
    pl.text(0.2,0.8,'Itcpt: '+str(round(aax,5))+r'$\pm$'+str(round(SEax,5)),transform = ax.transAxes)
    pl.text(0.2,0.75,'Chi2: '+str(round(chi2x,5)),transform = ax.transAxes)
    pl.ylim(-30,30)
    pl.xlim(-3100,3100)
    pl.title('0 degree position')
    pl.savefig('hex_z_move_zenith_ext_'+str(k)+'.png')
    #pl.savefig('hex_z_move_0degree_ext_'+str(k)+'.png')
    pl.close()
