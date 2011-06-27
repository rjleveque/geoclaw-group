c=========================================================================
      subroutine setprob
c=========================================================================

      use geoclaw_module
      use topo_module
      use dtopo_module

      implicit double precision (a-h,o-z)
      common /wave/ profile(451,2)


      call set_geo          !# sets basic parameters g and coord system
      call set_tsunami      !# sets parameters specific to tsunamis
      call set_topo         !# specifies topography (bathymetry) files
      call set_dtopo        !# specifies file with dtopo from earthquake
      call setqinit         !# specifies file with dh if this used instead
      call setregions       !# specifies where refinement is allowed/forced
      call setgauges        !# locations of measuring gauges
      call setfixedgrids    !# specifies output on arbitrary uniform fixed grids

      
      open(unit=76,file='../wave.txt',status='old',form='formatted')

      do it=1,451
         read(76,*) profile(it,1),profile(it,2)
      enddo
      close(unit=76)

      return
      end
