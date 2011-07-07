

c     =====================================================
       subroutine qinit(maxmx,maxmy,meqn,mbc,mx,my,xlower,ylower,
     &                   dx,dy,q,maux,aux)
c     =====================================================
c
c      # Set initial sea level flat unless iqinit = 1, in which case
c      # an initial perturbation of the q(i,j,1) is specified and has
c      # been strored in qinitwork.


       use geoclaw_module
       use dz_module

       implicit double precision (a-h,o-z)
       dimension q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)
       dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc,maux)

       dxfine = dmin1(dxfine,dx)  ! will end up being dx on finest grid level.
                                  ! used in b4step2.

       write(35,*) 'dxfine: ',dxfine

       ! Topo is set in b4step2:
       t = 0.d0
       call b4step2(maxmx,maxmy,mbc,mx,my,meqn,q,
     &            xlower,ylower,dx,dy,t,dt,maux,aux)

       do i=1-mbc,mx+mbc
          x = xlower + (i-0.5d0)*dx
          do j=1-mbc,my+mbc
             y = ylower + (j-0.5d0)*dy
             q(i,j,1)=dmax1(0.d0,sealevel-aux(i,j,1))
             q(i,j,2)=0.d0
             q(i,j,3)=0.d0
             enddo
          enddo


       return
       end
