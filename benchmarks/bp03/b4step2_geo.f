c     ============================================
      subroutine b4step2(maxmx,maxmy,mbc,mx,my,meqn,q,
     &            xlower,ylower,dx,dy,t,dt,maux,aux)
c     ============================================
c
c     # called before each call to step
c     # use to set time-dependent aux arrays or perform other tasks.
c
c     Set moving bathy for landslide problem.
c
c     This particular routine sets negative values of q(i,j,1) to zero,
c     as well as the corresponding q(i,j,m) for m=1,meqn.
c     This is for problems where q(i,j,1) is a depth.
c     This should occur only because of rounding error.

c     Also calls movetopo if topography might be moving.

      use geoclaw_module
      use topo_module
      use dtopo_module
      use dz_module

      implicit double precision (a-h,o-z)

      common /comrunup/ ybar1,ybar2

      dimension q(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, meqn)
      dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, maux)

      integer istatus
      character*25 bfname
      double precision bt,bx
c=====================Parameters===========================================


      if (dx <= dxfine) then
         ! only do this on finest grid
         do i = 1,mx
c           write(33,331) t, i, q(i,jbar,1)
c331        format(e16.6,i5,e16.6)
              if (q(i,1,1)<0.001) then
                  i1 = i
              endif
              if (q(i,1,1)<0.0005) then
                  i2 = i
              endif
         enddo
         runup1 = tanth*(xlower + i1*dx)
         runup2 = tanth*(xlower + i2*dx)
         write(32,40) t,runup1,runup2
40       format(3e20.10)
      endif

c     # Set moving bathymetry
c     # Many parameters and variables below are set in dz_module.

      s = s_fcn(t)
      xi0 = x0 / costh
      xic = xi0 + s
      !write(26,*) "+++ t = ",t,"  xc = ",xic
      xc = xic*costh
      tol = 1.d-6      ! tolerance for zeroin
      
      do j=1-mbc,my+mbc
         y = ylower + (j-0.5d0)*dy
         eta = y
         do i=1-mbc,mx+mbc
            x = xlower + (i-0.5d0)*dx
            z = -x * tanth   ! slope with no mass
            if ((dabs(x-xc) < xlength) .and. (eta < width)) then
                ! region of landslide mass
                x4zeroin = x      ! module parameter used in fxi
                eta4zeroin = eta  ! module parameter used in fxi
                axi = xic - length
                bxi = xic + length
                xi = zeroin(axi,bxi,fxi,tol)
                zeta = zeta_fcn(xi-xic, eta)
                x2 = xi*costh + zeta*sinth
                z = -xi*sinth + zeta*costh
                if (dabs(x-x2) > tol) then
                    write(6,*) "*** Error?  x = ",x,"  x2 = ",x2
                    write(6,*) "*** xi = ", xi, "  axi = ",axi, 
     &                         "   bxi = ",bxi
                endif
             endif
             aux(i,j,1) = dmax1(z, -1.5d0)
             
        enddo
      enddo


c     # check for NANs in solution:
      call check4nans(maxmx,maxmy,meqn,mbc,mx,my,q,t,1)

c     # check for h < 0 and reset to zero
c     # check for h < drytolerance
c     # set hu = hv = 0 in all these cells

      do i=1-mbc,mx+mbc
        do j=1-mbc,my+mbc
          if (q(i,j,1).lt.drytolerance) then
             q(i,j,1) = max(q(i,j,1),0.d0)
             do m=2,meqn
                q(i,j,m)=0.d0
                enddo
             endif
        enddo
      enddo

      write(26,*) 'B4STEP2: t, num_dtopo: ', t,num_dtopo
      do i=1,num_dtopo
          call movetopo(maxmx,maxmy,mbc,mx,my,
     &      xlower,ylower,dx,dy,t,dt,maux,aux,
     &      dtopowork(i0dtopo(i):i0dtopo(i)+mdtopo(i)-1),
     &      xlowdtopo(i),ylowdtopo(i),xhidtopo(i),yhidtopo(i),
     &      t0dtopo(i),tfdtopo(i),dxdtopo(i),dydtopo(i),dtdtopo(i),
     &      mxdtopo(i),mydtopo(i),mtdtopo(i),mdtopo(i),
     &      minleveldtopo(i),maxleveldtopo(i),topoaltered(i))
      enddo


      return
      end


