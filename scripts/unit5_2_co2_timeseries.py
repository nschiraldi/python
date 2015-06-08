# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:33:23 2015

@author: oe524132
"""

# CO2 fitting trends and seasonal cycle
import numpy as np
import pylab as pl
data=np.loadtxt("../data/co2_mm_mlo.txt",usecols=(0,1,2,4))
time=data[:,2]
co2=data[:,3]
pl.plot(time,co2,'gray')
pl.xlabel('year')
pl.ylabel('CO2 concentration [ppmv]')



# fitting a linear trend
# we consider the time information as a time series
# pl.plot(time,time) 

# the linear regression problem is to find the slope and intercept
# we have seen the mathematical solution is

# slope b= correlation * std(y)/std(x)
# here x is the time series of time information itself 
# and y is the CO2 time series

from unit3_5_matrix_calculus import *

tmean=vectorMean(time)
tstd=np.sqrt(vectorCov(time,time))

ymean=vectorMean(co2)
ystd=np.sqrt(vectorCov(co2,co2))

r=vectorCor(time,co2)
print '-------------------'
print 'Summary statistics:'
print '-------------------'
print 'time mean %8.3f' % (tmean)
print 'CO2 mean %8.3f' % (ymean)
print "'standard deviation' of the time index time series %8.3f" %(tstd)
print 'standard deviation of the CO2 time series %8.3f' %(ystd)
print 'correlation of CO2 with linear trend line %6.3f' %(r) 


# intercept a , slope b of linear trend line
b=r*ystd/tstd
a=ymean-b*tmean
# fitted line
trend=a+b*time
pl.plot(time,trend,color='red',linewidth=3,alpha=0.9)
print 'fitting parameters for regressed linear trend line:'  
print 'CO2 = %8.3f +  %8.4f*year' %(a,b)
# residuals 
resid=co2-trend
print 'Standard devation in the residuals (deviations from the trend): '
print '%8.4f' %(np.sqrt(vectorCov(resid,resid)))


###########################################################################
# compare with scipy.stats function linregress
###########################################################################
if True:
    print '++++++++++++++++++++++++++++++++++++++++++++++++'
    print 'compare with the scipy.stats.linregress function'
    print '++++++++++++++++++++++++++++++++++++++++++++++++'
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(time,co2)
    print 'r value', r_value
    print  'p_value', p_value
    print 'standard deviation', std_err
    print 'slope ', slope
    print 'intercept' , intercept
    line = slope*time+intercept
    pl.plot(time,line,'y-',alpha=0.9,linewidth=3)

