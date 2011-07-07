
module dz_module

    ! Module parameters:

    real(kind=8), parameter :: theta = 15.d0 * acos(-1.d0) / 180.d0
    real(kind=8), parameter :: costh = cos(theta)
    real(kind=8), parameter :: sinth = sin(theta)
    real(kind=8), parameter :: tanth = tan(theta)

    real(kind=8), parameter :: width = 0.680d0
    real(kind=8), parameter :: length = 0.395d0
    real(kind=8), parameter :: xlength = length*costh

    real(kind=8), parameter :: epsilon = 0.717d0
    real(kind=8), parameter :: C = acosh(1. / epsilon)
    real(kind=8), parameter :: Tprime = 0.082 + 0.004d0
    real(kind=8), parameter :: kb = 2*C / length
    real(kind=8), parameter :: kw = 2*C / width


    ! Module variables:

    real(kind=8) :: x4zeroin, eta4zeroin, xic, d, x0, dxfine
    real(kind=8), dimension(100) :: tk
    real(kind=8), dimension(100,7) :: sk
    integer :: scolumn 

    save

contains

  real (kind=8) function zeta_fcn(xi, eta)
      implicit none
      real (kind=8), intent(in) :: xi,eta

      zeta_fcn = dmax1(0.d0,  (Tprime/(1.-epsilon)) * &
                 (1./(cosh(kb*xi)*cosh(kw*eta)) - epsilon))

  end function zeta_fcn

    
  subroutine read_ts()
      ! Read the data file and set tk and sk arrays.
      implicit none
      integer :: i, k
      open(unit=10,file='../kinematics-new.txt',status='old',form='formatted')

      do i=1,100
         read(10,*) tk(i),(sk(i,k),k=1,7)
         !write(6,*) i,tk(i),sk(i,1)
      enddo
  end subroutine read_ts


  real (kind=8) function s_fcn(t)
      ! Interpolate from sk array to the current time.
      ! Use column of sk determined by scolumn.
      implicit none
      real (kind=8), intent(in) :: t
      real (kind=8) :: dtk
      integer :: k

      k = min(100, int(t*10)+1)
      dtk = 0.1d0
      s_fcn = (sk(k,scolumn)*(tk(k+1)-t) + sk(k+1,scolumn)*(t-tk(k))) / dtk
      write(26,*) "+++ t,k,dtk,sk,s_fcn: ",t,k,dtk,sk(k,scolumn),s_fcn
      

  end function s_fcn


  real (kind=8) function fxi(xi)
      ! Function we will apply zeroin to in order to find xi 
      ! corresponding to a given x value.

      implicit none
      real (kind=8), intent(in) :: xi

      fxi = xi*costh + zeta_fcn(xi - xic, eta4zeroin)*sinth - x4zeroin

  end function fxi


end module dz_module
