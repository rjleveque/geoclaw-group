c     ============================================
      subroutine b4step2(maxmx,maxmy,mbc,mx,my,meqn,q,
     &            xlower,ylower,dx,dy,t,dt,maux,aux)
c     ============================================
c
c     # called before each call to step
c     # use to set time-dependent aux arrays or perform other tasks.
c
c     This particular routine sets negative values of q(i,j,1) to zero,
c     as well as the corresponding q(i,j,m) for m=1,meqn.
c     This is for problems where q(i,j,1) is a depth.
c     This should occur only because of rounding error.

c     Also calls movetopo if topography might be moving.

      use geoclaw_module
      use topo_module
      use dtopo_module

      implicit double precision (a-h,o-z)

      common /comrunup/ ybar1,ybar2

      dimension q(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, meqn)
      dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, maux)

      integer istatus
      character*25 bfname
      double precision bt,bx
c=====================Parameters===========================================


        if (dx < 0.02)then
           jbar1 = (ybar1 - ylower)/dy + 1
           jbar2 = (ybar2 - ylower)/dy + 1
           do i = 1,mx
c        write(33,331) t, i, q(i,jbar,1)
c331     format(e16.6,i5,e16.6)
              if (q(i,jbar1,1)<0.001) then
                  i1 = i
              endif
              if (q(i,jbar2,1)<0.001) then
                  i2 = i
              endif
          enddo
          runup1 = 0.5*(xlower + i1*dx)
          runup2 = 0.5*(xlower + i2*dx)
          write(32,40) t,runup1,runup2
40        format(3e20.10)
        endif


      bfname="../block1.tx"

      if (t.lt.3.5d0) then
         open(unit=45,file=bfname,status='old',form='formatted') !note: should probably read file into an array once
         do k=1,701
            read(45,fmt=*,iostat=istatus) bt,bx
            if (bt.ge. t) then !Note: this is a bit crude...should probably interpolate between two bt
                               !bt is the time column of block
               xb1 = 0.01d0*bx + 0.05d0 !position of the start of the block
               close(45)
               exit
            endif
         enddo
      else
         xb1 = 4.26181624 + .05 !position of start of the block after stopping
      endif

      do i=1,mx
         do j=1,my
            x = xlower + (i-0.5d0)*dx
            y = ylower + (j-0.5d0)*dy
            if (abs(y).le.0.305) then
               if ((x.ge.xb1).and.(x.le.xb1+0.91)) then !region of block
                  aux(i,j,1) = -0.5*xb1 !block is flat on top
               else
                  aux(i,j,1) = -.5*x !in front of or behind block: tank bathy
               endif
            else
                  aux(i,j,1) = -.5*x !to the side of the block: tank bathy
            endif
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


