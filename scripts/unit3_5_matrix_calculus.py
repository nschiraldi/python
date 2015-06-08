# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:21:57 2015

@author: Oliver Elison Timm
"""

# for educational purposes, I tried on purpose to 
# work with numpy arrays of 2 dimensions 
# to illustrate the calculation needed to obtain 
# the mean (column-wise)
# and the covariance matrix and correlation matrix
# Implicit Rule: rows are samples from repeated observations
# or experiments, and columns contain various variables

import numpy as np

############################################################################
# Vector calculations
############################################################################

def rmNANv(x):
    """Removes all elements with NAN in a vector x."""
    isnan=np.isnan(x)
    isdata=np.logical_not(isnan)
    res=x[isdata]
    return res 

def vectorMean(x):
    """ use dot product to calculate the mean of the elements in a vector x.
    x is expected to be a numpy 1-d  array"""
    n=np.size(x)
    w=np.ones(n)
    res=np.dot(w,x)/n
    return res

def vectorCov(x,y):
    """ use dot product to calculate the covariance between x and y (vectors).
    x, y are expected to be a numpy 1-d  array"""
    isnanx=np.isnan(x)
    isnany=np.isnan(y)
    isnan=np.logical_or(isnanx,isnany)
    isuse=np.logical_not(isnan)
    xuse=x[isuse]
    yuse=y[isuse]
    nuse=np.size(xuse)
    xm=vectorMean(xuse)
    ym=vectorMean(yuse)
    # numpy array applies addition, multiplication with scalars on vectors
    # for each element, here we center the data
    xuse=xuse-xm
    yuse=yuse-ym
    if (nuse>0):
        res=np.dot(xuse,yuse)/(nuse-1)
    return res


def vectorCor(x,y):
    """ use dot product to calculate the covariance between x and y (vectors).
    x, y are expected to be a numpy 1-d  array"""
    isnanx=np.isnan(x)
    isnany=np.isnan(y)
    isnan=np.logical_or(isnanx,isnany)
    isuse=np.logical_not(isnan)
    xuse=x[isuse]
    yuse=y[isuse]
    nuse=np.size(xuse)
    xm=vectorMean(xuse)
    ym=vectorMean(yuse)
    # numpy array applies addition, multiplication with scalars on vectors
    # for each element, here we center the data
    xuse=xuse-xm
    yuse=yuse-ym
    # use vectorCov to get the variance
    xycov=vectorCov(xuse,yuse)
    xvar=vectorCov(xuse,xuse)
    yvar=vectorCov(yuse,yuse)
    #print xm,ym,nuse,xvar,yvar
    if (nuse>0):
        res=xycov/np.sqrt(xvar*yvar)
    return res




#########################################################################
# traditional average function
#########################################################################


def traditionalMean(x):
    """ use explicit summation loop for averaging"""
    n=np.size(x)
    i=0
    res=0.0
    while i < n:
        res=res+x[i]
        i+=1
    res=res/n
    return res


def traditionalTiming(x):
    import time
    print 'performance test for speed:'
    print 'generate data sample of size n='+str(n)
    print 'start averaging with tradional mean function'
    d1=time.time()
    print d1
    res=traditionalMean(x)    
    d2=time.time()
    print 'end averaging at '
    print d2
    print 'duration: d2-d1 = '+str(d2-d1)+' seconds'
    return
    
def vectorTiming(x):
    import time
    n=np.size(x)
    print 'performance test for speed:'
    print 'generate data sample of size n='+str(n)
    print 'start averaging with vector mean function'
    d1=time.time()
    print d1
    res=vectorMean(x)
    d2=time.time()
    print 'end averaging at '    
    print d2
    print 'duration: d2-d1 = '+str(d2-d1)+' seconds'
    return
    



#########################################################################
# Matrix calculations
#########################################################################
    

def isMatrix(M):
    """Functions tests if our object is a Matrix.
    A Matrix must be 2-dimensional in shape, and of type numpy.darray
    or a special matrix-style object"""
    res=False
    if type(M)==np.ndarray :
        if (np.size(np.shape(M))==2):
            res=True
    return res
    
    
def rmNAN(M):
    """Removes all rows with NAN in a 2-dimensional array M.
    (M is a matrix)"""
    if isMatrix(M):
        isnan=np.any(np.isnan(M),1)
        isdata=np.logical_not(isnan)
        res=M[isdata,:]
    else:
        print "rmNAN(M): works only with matrix objects"
        res=np.NAN
    return res 
   

def columnMean(M):
    """Calculates with dot product the column mean values of a matrix M
    Note: no check for NAN is done"""
    if isMatrix(M):
        n=np.shape(M)[0] # number of rows
        W=np.reshape(np.repeat(1./n,n),[1,n])# 1 x n matrix
        res=np.dot(W,M)
    else:
        print "columnMean(M): works only with matrix objects"
        res=np.NAN
    return res[0,:] #return a 1-d array
    
def columnVar(M):
    """Calculates with dot product the column variance values of a matrix M
    Note: no check for NAN is done"""
    if isMatrix(M):
        n=np.shape(M)[0] # number of rows
        k=np.shape(M)[1]
        M=M-columnMean(M)
        i=0
        res=np.empty(k)
        while i<k:
            res[i]=np.dot(M[:,i],M[:,i])
            i+=1
        
        res=res/(n-1) # bessel correction 1/(n-1)
    else:
        print "columnVar(M): works only with matrix objects"
        res=np.NAN
    return res
    
def covarMatrix(M):
    """Calculates the covariance matrix with the matrix 
    dot product.
    Input:  M  n x k matrix
    Output: t(Mo) dot Mo, where Mo is the data matrix
    M minus the mean values in each column (centered data) 
    Note: no check for NAN is done
    Per default 'Bessel correction' is used (divide by 1/(n-1))"""
    if isMatrix(M):
        n=np.shape(M)[0] # number of rows
        mean=columnMean(M)
        # remove column by column the mean
        M=M-mean # numpy array repeats subtraction for each row!
        # now use dot product to do the variance
        res=1./(n-1)*np.dot(np.transpose(M),M)
    else:
        print "CovarMatrix(M): works only with matrix objects"
        res=np.NAN
    return res  
    
def correlMatrix(M):
    """Calculates the correlation matrix with the matrix 
    dot product.
    Input:  M  n x k matrix
    Output: t(Mo) dot Mo, where Mo is the data matrix
    M minus the mean values in each column (centered data) 
    Note: no check for NAN is done
    Per default 'Bessel correction' is used (divide by 1/(n-1))"""
    if isMatrix(M):
        n=np.shape(M)[0] # number of rows
        mean=columnMean(M)
        var=columnVar(M)
        # remove column by column the mean and divide by sqrt(var)
        # => z-score data        
        M=(M-mean)/np.sqrt(var) # numpy array repeats subtraction for each row!
        # now use dot product to do the variance
        res=1./(n-1)*np.dot(np.transpose(M),M)
    else:
        print "CorMatrix(M): works only with matrix objects"
        res=np.NAN
    return res      