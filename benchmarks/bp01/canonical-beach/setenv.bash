export CLAW='/Users/paulchamberlain/clawpack/branches/4.6.x'
export FC='gfortran'

export MATLABPATH='/Users/paulchamberlain/clawpack/trunk/matlab:/Users/paulchamberlain/clawpack/branches/4.5.x/matlab:/Users/paulchamberlain/clawpack/branches/5.0.x/matlab:/Users/paulchamberlain/clawpack/branches/4.6.x/matlab'

export PYTHONPATH='/Users/paulchamberlain/clawpack/branches/4.6.x/python:/Users/paulchamberlain/clawpack/branches/5.0.x/python:/Users/paulchamberlain/clawpack/branches/4.5.x/python:/Users/paulchamberlain/clawpack/trunk/python'
export IPYTHONDIR='/Users/paulchamberlain/clawpack/branches/4.6.x/python/ipythondir'
if [ -z "${DYLD_LIBRARY_PATH}" ]; then
    DYLD_LIBRARY_PATH="/Users/paulchamberlain/clawpack/branches/4.6.x/lib"
else
    DYLD_LIBRARY_PATH="/Users/paulchamberlain/clawpack/branches/4.6.x/lib:${DYLD_LIBRARY_PATH}"
fi
alias ipyclaw='ipython -profile claw' 
alias clawserver='xterm -e python $CLAW/python/startserver.py &' 
