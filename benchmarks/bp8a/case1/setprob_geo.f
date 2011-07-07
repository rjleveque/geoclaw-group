c=========================================================================
      subroutine setprob
c=========================================================================

      use geoclaw_module
      use topo_module
      use dtopo_module

      implicit double precision (a-h,o-z)

      common /comrunup/ ybar1,ybar2

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
