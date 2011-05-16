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
    pl.figure(figsize=(15,8))
    pl.subplot(1,2,1)
    pl.plot(x0,y0,'bo')
    pl.plot(x1[i1],y1[i1],'r.')
    pl.xlim(0,2400)
    pl.ylim(0,4500)
    pl.subplot(1,2,2)
    pl.plot(x1,y1,'bo')
    pl.plot(x0[i0],y0[i0],'r.')
    pl.xlim(0,2400)
    pl.ylim(0,4500)
    pl.show()
