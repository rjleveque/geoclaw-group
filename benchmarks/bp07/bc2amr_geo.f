
c
c ------------------------------------------------------------------
c
      subroutine bc2amr(val,aux,nrow,ncol,meqn,naux,
     1                  hx, hy, level, time, 
     2                  xleft,  xright,  ybot, ytop,
     3                  xlower, ylower,xupper,yupper,
     4                  xperiodic, yperiodic,spheredom)
 
c
c    Specific to geoclaw:  extrapolates aux(i,j,1) at boundaries
c    to constant.
c
c :::::::::: bc2amr ::::::::::::::::::::::::::::::::::::::::::::::;
c
c     Take a grid patch with mesh widths hx,hy, of dimensions nrow by
c     ncol,  and set the values of any piece of
c     of the patch which extends outside the physical domain 
c     using the boundary conditions. 
c
c     ------------------------------------------------
c     # Standard boundary condition choices for amr2ez in clawpack
c
c     # At each boundary  k = 1 (left),  2 (right),  3 (top), 4 (bottom):
c     #   mthbc(k) =  0  for user-supplied BC's (must be inserted!)
c     #            =  1  for zero-order extrapolation
c     #            =  2  for periodic boundary coniditions
c     #            =  3  for solid walls, assuming this can be implemented
c     #                  by reflecting the data about the boundary and then
c     #                  negating the 2'nd (for k=1,2) or 3'rd (for k=3,4)
c     #                  component of q.
c     #            =  4  sphere bcs (left half maps to right half of same 
c     #                  side, and vice versa), as if domain folded in half
c     ------------------------------------------------
c
c     The corners of the grid patch are at 
c        (xleft,ybot)  --  lower left corner
c        (xright,ytop) --  upper right corner
c
c     The physical domain itself is a rectangle bounded by
c        (xlower,ylower)  -- lower left corner
c        (xupper,yupper)  -- upper right corner
c     
c     the picture is the following: 
c
c               _____________________ (xupper,yupper)
c              |                     |  
c          _________ (xright,ytop)   |
c          |   |    |                |
c          |   |    |                |
c          |   |    |                |
c          |___|____|                |
c (xleft,ybot) |                     |
c              |                     |
c              |_____________________|
c   (xlower,ylower)
c        
c
c     Any cells that lie outside the physical domain are ghost cells whose
c     values should be set in this routine.  This is tested for by comparing
c     xleft with xlower to see if values need to be set at the left, as in
c     the figure above, and similarly at the other boundaries.
c
c     Patches are guaranteed to have at least 1 row of cells filled
c     with interior values so it is possible to  extrapolate. 
c     Fix trimbd if you want more than 1 row pre-set.
c
c     Make sure the order the boundaries are specified is correct
c     so that diagonal corner cells are also properly taken care of.
c
c     Periodic boundaries are set before calling this routine, so if the
c     domain is periodic in one direction only you
c     can safely extrapolate in the other direction. 
c
c     Don't overwrite ghost cells in periodic directions!

c     This particular routine bc2amr_noslopesets auxillary values so 
c     that no slope in topography occurs at the physical boundary.
c
c ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;

      implicit double precision (a-h,o-z)

      common /wave/ profile(451,2)
      common /combc2/ mthbc(4)

      dimension val(nrow,ncol,meqn), aux(nrow,ncol,naux)
      logical xperiodic, yperiodic, spheredom

      hxmarg = hx*.01
      hymarg = hy*.01

      if (xperiodic .and. (yperiodic .or. spheredom)) go to 499
c
c
c-------------------------------------------------------
c     # left boundary:
c-------------------------------------------------------
      if (xleft .ge. xlower-hxmarg) then
c        # not a physical boundary -- no cells at this edge lies
c        # outside the physical bndry.
c        # values are set elsewhere in amr code.
         go to 199
         endif
c
c     # number of grid cells from this patch lying outside physical domain:
      nxl = (xlower+hxmarg-xleft)/hx
c
      go to (100,110,120,130) mthbc(1)+1
c
  100 continue
c     # Specify a wave entering the domain given by profile stored
c     # in common block:

      t = time
      if (t.ge.21.5d0) then
c        # switch to nonreflecting BC after wave has entered:
         go to 110
      endif


c     # values in ghost cell at x = -epsilon  should
c     # be set to values at point x=0 at time t + epsilon / speed
c     # where speed = sqrt(gh) is the wave speed.
c     # Use undisturbed state h0 = 13.5 cm.

      h0 = 0.135d0
      grav = 9.81d0  !# should fix to use value in module!
      speed = dsqrt(grav*h0)

      t1 = t + 0.5d0*hx / speed  ! ghost cell adjecent to boundary
      t2 = t + 1.5d0*hx / speed  ! next ghost cell away from boundary
      
c     # interpolate profile to find surface level eta at these times:
      
      do it=1,450
         if (profile(it,1).le.t1.and.profile(it+1,1).gt.t1) then
            etaslope1=(profile(it+1,2)-profile(it,2))/.05d0
            eta1=profile(it,2)+ etaslope1*(t1-profile(it,1))
            
            do it2=it,450
                if (profile(it2,1).le.t2.and.
     &                    profile(it2+1,1).gt.t2) then
                   etaslope2=(profile(it2+1,2)-profile(it2,2))/.05d0
                   eta2=profile(it2,2)+ etaslope2*(t2-profile(it2,1))
                
                   go to 101
                 endif
               enddo
               
         endif
      enddo 
      write(*,*) 't2 is out of range',profile(it2,1),t2,profile(it2+1,1)
      stop
 101  continue
c     write(46,*) 't1 = ',t1,'   it  = ',it,'  eta1 = ',eta1
c     write(46,*) '  profiles: ',profile(it,2),profile(it+1,2)
c     write(46,*) '  etaslopes: ',etaslope1,etaslope2
c     write(46,*) 't2 = ',t2,'   it2 = ',it2,'  eta1 = ',eta2
      
 

c     # Riemann invariant for right-going wave:
c     # u - 2*sqrt(gh) is constant with value rinvar given by undisturbed
c     # state with depth h0 and zero velocity:
      rinvar=-2.0d0*sqrt(grav*h0)

      do 105 j=1,ncol
c        # depth h = eta - B:
         h1 = eta1 - aux(nxl+1,j,1)
c        # velocity found using Riemann invariant: 
c        #   u - 2*sqrt(gh) = rinvar:           
         u1 = 2.d0*sqrt(grav*h1)+rinvar
         
         if (nxl == 1) then
c            # only one ghost cell:
             aux(1,j,1) = aux(nxl+1,j,1)  
             val(1,j,1) = h1
             val(1,j,2) = h1*u1
             val(1,j,3) = 0.d0
          else
c            # two ghost cells:
             aux(2,j,1) = aux(nxl+1,j,1)  
             val(2,j,1) = h1
             val(2,j,2) = h1*u1
             val(2,j,3) = 0.d0
             
             h2 = eta2 - aux(nxl+1,j,1)     
             u2 = 2.d0*sqrt(grav*h2)+rinvar
             aux(1,j,1) = aux(nxl+1,j,1)              
             val(1,j,1) = h2
             val(1,j,2) = h2*u2
             val(1,j,3) = 0.d0
          endif

 105    continue
c     write(47,*) t1,val(1,2,1),val(1,2,2)
c     write(48,*) t1,val(2,2,1),val(2,2,2)
      
      
      go to 199
c
c
  110 continue
c     # zero-order extrapolation:
      do 115 m=1,meqn
         do 115 i=1,nxl
            do 115 j = 1,ncol
               aux(i,j,1) = aux(nxl+1,j,1)  !inserted for bc2amr_noslope
               val(i,j,m) = val(nxl+1,j,m)
  115       continue
      go to 199

  120 continue
c     # periodic:   handled elsewhere in amr
      go to 199

  130 continue
c     # solid wall (assumes 2'nd component is velocity or momentum in x):
      do 135 m=1,meqn
         do 135 i=1,nxl
            do 135 j = 1,ncol
               aux(i,j,1) = aux(2*nxl+1-i,j,1)  !inserted for bc2amr_noslope
               val(i,j,m) = val(2*nxl+1-i,j,m)
  135       continue
c     # negate the normal velocity:
      do 136 i=1,nxl
         do 136 j = 1,ncol
            val(i,j,2) = -val(i,j,2)
  136    continue
      go to 199

  199 continue
c
c-------------------------------------------------------
c     # right boundary:
c-------------------------------------------------------
      if (xright .le. xupper+hxmarg) then
c        # not a physical boundary --  no cells at this edge lies
c        # outside the physical bndry.
c        # values are set elsewhere in amr code.
         go to 299
         endif
c
c     # number of grid cells lying outside physical domain:
      nxr = (xright - xupper + hxmarg)/hx
      ibeg = max0(nrow-nxr+1, 1)
c
      go to (200,210,220,230) mthbc(2)+1
c
  200 continue
c     # user-specified boundary conditions go here in place of error output
      write(6,*) 
     &   '*** ERROR *** mthbc(2)=0 and no BCs specified in bc2amr'
      stop
      go to 299

  210 continue
c     # zero-order extrapolation:
      do 215 m=1,meqn
         do 215 i=ibeg,nrow
            do 215 j = 1,ncol
               aux(i,j,1) = aux(ibeg-1,j,1) !inserted for bc2amr_noslope
               val(i,j,m) = val(ibeg-1,j,m)
  215       continue
      go to 299

  220 continue
c     # periodic:   handled elsewhere in amr
      go to 299

  230 continue
c     # solid wall (assumes 2'nd component is velocity or momentum in x):
      do 235 m=1,meqn
         do 235 i=ibeg,nrow
            do 235 j = 1,ncol
               aux(i,j,1) = aux(2*ibeg-1-i,j,1) !inserted for bc2amr_noslope
               val(i,j,m) = val(2*ibeg-1-i,j,m)
  235       continue
c     # negate the normal velocity:
      do 236 i=ibeg,nrow
         do 236 j = 1,ncol
            val(i,j,2) = -val(i,j,2)
  236    continue
      go to 299

  299 continue
c
c-------------------------------------------------------
c     # bottom boundary:
c-------------------------------------------------------
      if (ybot .ge. ylower-hymarg) then
c        # not a physical boundary -- no cells at this edge lies
c        # outside the physical bndry.
c        # values are set elsewhere in amr code.
         go to 399
         endif
c
c     # number of grid cells lying outside physical domain:
      nyb = (ylower+hymarg-ybot)/hy
c
      go to (300,310,320,330) mthbc(3)+1
c
  300 continue
c     # user-specified boundary conditions go here in place of error output
      write(6,*) 
     &   '*** ERROR *** mthbc(3)=0 and no BCs specified in bc2amr'
      stop
      go to 399
c
  310 continue
c     # zero-order extrapolation:
      do 315 m=1,meqn
         do 315 j=1,nyb
            do 315 i=1,nrow
                aux(i,j,1) = aux(i,nyb+1,1) !inserted for bc2amr_noslope
                val(i,j,m) = val(i,nyb+1,m)
  315       continue
      go to 399

  320 continue
c     # periodic:   handled elsewhere in amr
      go to 399

  330 continue
c     # solid wall (assumes 3'rd component is velocity or momentum in y):
      do 335 m=1,meqn
         do 335 j=1,nyb
            do 335 i=1,nrow
                aux(i,j,1) =  aux(i,2*nyb+1-j,1) !inserted for bc2amr_noslope
                val(i,j,m) =  val(i,2*nyb+1-j,m)
  335       continue
c     # negate the normal velocity:
      do 336 j=1,nyb
         do 336 i=1,nrow
            val(i,j,3) = -val(i,j,3)
  336    continue
      go to 399

  399 continue
c
c-------------------------------------------------------
c     # top boundary:
c-------------------------------------------------------
      if (ytop .le. yupper+hymarg) then
c        # not a physical boundary --  no cells at this edge lies
c        # outside the physical bndry.
c        # values are set elsewhere in amr code.
         go to 499
         endif
c
c     # number of grid cells lying outside physical domain:
      nyt = (ytop - yupper + hymarg)/hy
      jbeg = max0(ncol-nyt+1, 1)
c
      go to (400,410,420,430) mthbc(4)+1
c
  400 continue
c     # user-specified boundary conditions go here in place of error output
      write(6,*) 
     &   '*** ERROR *** mthbc(4)=0 and no BCs specified in bc2amr'
      stop
      go to 499

  410 continue
c     # zero-order extrapolation:
      do 415 m=1,meqn
         do 415 j=jbeg,ncol
            do 415 i=1,nrow
               aux(i,j,1) = aux(i,jbeg-1,1)  !inserted for bc2amr_noslope
               val(i,j,m) =  val(i,jbeg-1,m)
  415       continue
      go to 499

  420 continue
c     # periodic:   handled elsewhere in amr
      go to 499

  430 continue
c     # solid wall (assumes 3'rd component is velocity or momentum in y):
      do 435 m=1,meqn
         do 435 j=jbeg,ncol
            do 435 i=1,nrow
               aux(i,j,1) =  aux(i,2*jbeg-1-j,1)  !inserted for bc2amr_noslope
               val(i,j,m) =  val(i,2*jbeg-1-j,m)
  435       continue
c     # negate the normal velocity:
      do 436 j=jbeg,ncol
         do 436 i=1,nrow
            val(i,j,3) = -val(i,j,3)
  436    continue
      go to 499

  499 continue

      return
      end

