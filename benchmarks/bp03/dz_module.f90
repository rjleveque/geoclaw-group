
module dz_module

    real(kind=8), parameter :: dyk = 0.01d0
    real(kind=8), parameter :: dxik = 0.001d0
    real(kind=8), parameter :: theta = 15.d0 * acos(-1.d0) / 180.d0
    real(kind=8), parameter :: width = 0.680d0
    real(kind=8), parameter :: length = 0.395d0
    real(kind=8), parameter :: epsilon = 0.717d0
    real(kind=8), parameter :: C = acosh(1. / epsilon)
    real(kind=8), parameter :: T = 0.082
    real(kind=8), parameter :: kb = 2*C / length
    real(kind=8), parameter :: kw = 2*C / width


    integer, parameter :: imax = length/dxik + 1
    integer, parameter :: jmax = 0.5d0*width / dyk + 1

    real(kind=8), dimension(imax,jmax) :: dzk
    real(kind=8), dimension(100) :: tk
    real(kind=8), dimension(100,7) :: sk

    save

contains

  subroutine compute_dzk()

      implicit double precision (a-h,o-z)

      do j=1,jmax
         eta = ylower + (j-0.5d0)*dyk
         do i=1,imax
            xi = -0.5d0*length + (i-1)*dxk
            zeta1 = (T/(1.-epsilon)) * (1./(cosh(kb*xi)*cosh(kw*eta)) - epsilon)
            zeta = dmax1(zeta1, 0.d0)
            xk(i,j) =  cos(theta)*xi + sin(theta)*zeta
            z       = -sin(theta)*xi + cos(theta)*zeta
            dzk(i,j) = z - (-tan(theta)*xk(i,j))
            enddo
         enddo

  end subroutine compute_dzk
    
  subroutine read_ts()

      implicit double precision (a-h,o-z)

      open(unit=10,file='kinematics-new.txt')
      do i=1,100
        read(10,*) tk(i),(sk(i,k),k=1,7)
        enddo
  end subroutine read_ts


  subroutine compute_dz(maxmx,maxmy,xlower,ylower,dx,dy,mx,my,t,dz)

      implicit double precision (a-h,o-z)

      real(kind=8) :: dz(maxmx,maxmy)

      dz = 0.d0

      k = 1
      do while (tk(k) <= t)
         k = k+1
         enddo
      s = ((t-tk(k-1))*sk(k-1) + (tk(k)-t)*sk(k)) / (tk(k)-tk(k-1))

      xc = x0 + s*

      do j=1,jmax
         y = ylower + (j-0.5d0)*dy
         
         k = 1
         do i=1,mx
            x = xlower + (i-0.5d0)*dx
            xs = x - xc
            if (dabs(xs) <= 0.1d0) then
                do while (xk(k) < xs)
                    k = k+1
                    enddo
                dz(i,j) = ((xs-xk(k-1))*dzk(k-1,j) + (xk(k)-xs)*dzk(k,j)) &
                             / (xk(k)-xk(k-1))
                endif
            enddo
        enddo
                

    end subroutine compute_dz

end module dz_module
