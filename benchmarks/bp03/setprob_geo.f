c=========================================================================
      subroutine setprob
c=========================================================================

      use geoclaw_module
      use topo_module
      use dtopo_module
      use dz_module

      implicit double precision (a-h,o-z)
      character*12 fname


      common /comrunup/ ybar1,ybar2

      ! Read tk and sk arrays needed in dz_module:
      call read_ts()

      ! Set dz_module variables:

      dxfine = 1.d0  ! will be set properly in qinit

      ! initial depth of mass:
      iunit = 7
      fname = 'setprob.data'
c     # open the unit with new routine from Clawpack 4.4 to skip over
c     # comment lines starting with #:
      call opendatafile(iunit, fname)

      read(7,*) d

      if (dabs(d-0.061d0) .lt. 1e-10) then
          scolumn = 1
      elseif (dabs(d-0.080d0) .lt. 1e-10) then
          scolumn = 2
      elseif (dabs(d-0.100d0) .lt. 1e-10) then
          scolumn = 3
      elseif (dabs(d-0.120d0) .lt. 1e-10) then
          scolumn = 4
      elseif (dabs(d-0.140d0) .lt. 1e-10) then
          scolumn = 5
      elseif (dabs(d-0.149d0) .lt. 1e-10) then
          scolumn = 6
      elseif (dabs(d-0.189d0) .lt. 1e-10) then
          scolumn = 7
      else
          write(6,*) "*** Error: Unrecognized d in setprob, d = ",d
          stop
      endif
        

      ! Initial x-location of mass:
      x0 = d/tanth + Tprime/sinth
      write(6,601) d, scolumn, x0
 601  format(" Using d = ",d10.3, "   experiment = ",i2, "  x0 = ",
     &   d10.3)

      ! Runup:

      ybar1 = 0.305
      ybar2 = 0.61

c      ylower = -1.85d0  !!!! fix this !!!!
c      dy = 2.d0*1.85 / 370  !! fix this

c      jbar1 = (ybar1 - ylower)/dy + 1
c      jbar2 = (ybar2 - ylower)/dy + 1

      open(unit=32,file='fort.runup')

      call set_geo          !# sets basic parameters g and coord system
      call set_tsunami      !# sets parameters specific to tsunamis
      call set_topo         !# specifies topography (bathymetry) files
      call set_dtopo        !# specifies file with dtopo from earthquake
      call setqinit         !# specifies file with dh if this used instead
      call setregions       !# specifies where refinement is allowed/forced
      call setgauges        !# locations of measuring gauges
      call setfixedgrids    !# specifies output on arbitrary uniform fixed grids

      return
      end
