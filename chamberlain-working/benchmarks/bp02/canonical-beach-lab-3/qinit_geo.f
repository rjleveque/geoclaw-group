

c     =====================================================
       subroutine qinit(maxmx,maxmy,meqn,mbc,mx,my,xlower,ylower,
     &                   dx,dy,q,maux,aux)
c     =====================================================
c
c      # Set initial sea level flat unless iqinit = 1, in which case
c      # an initial perturbation of the q(i,j,1) is specified and has
c      # been strored in qinitwork.


       implicit double precision (a-h,o-z)
       dimension q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)
       dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc,maux)


       hmax = 0.3d0
       gamma = dsqrt(0.75d0*hmax)
       xs = 25.d0

       do i=1-mbc,mx+mbc
          x = xlower + (i-0.5d0)*dx
          do j=1-mbc,my+mbc
             y = ylower + (j-0.5d0)*dy
             eta = 4.d0*hmax*(1.d0/(dexp(gamma*(x-xs)) 
     &             + dexp(-gamma*(x-xs))))**2
             q(i,j,1)=dmax1(0.d0,eta-aux(i,j,1))
             h0=dmax1(0.d0,-aux(i,j,1))
             q(i,j,2)=q(i,j,1)*2.d0*(dsqrt(h0) - dsqrt(q(i,j,1)))
             q(i,j,3)=0.d0
             enddo
          enddo


       return
       end
