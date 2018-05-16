#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 14:44:15 2018

This file is ment to start a generalization of creating a fine structure of the
data obtain from the oscilloscope.

@author: ccartagena
"""

import numpy as np
import pandas as pd
import matplotlib.pylab as plt

def dataload_csv(filename, headout = False):
    """
       This function is designed to take in the name of a csv-data file from 
       the oscilloscope in our lab.
               
               filename-parameter: (String)
               ::: The location and name of the file to be converted.
               
               headout-parameter: (True or False)
               ::: the parameter determines if the header should be outputed
                   in addition to the data. The datatype of the header is a 
                   datastructure.
    """
    if headout == True:
        data = pd.read_csv(filename, usecols = (3,4), header = None, 
                           names = ['Voltage', 'Time'])
        head = pd.read_csv(filename, usecols = (0,1), header = None,
                           names = ['Head1','Head2'])
        head = head.dropna()
        orglist = (data, head,)
    else:
        data = pd.read_csv(filename, usecols = (3,4), header = None,
                           names = ['Voltage', 'Time'])
        orglist = (data,)
        
    return orglist

#------------------------------------------------------------------------------
def headerload_csv(filename):
    """
        This function is designed to output solely the header of the data.
            
            filename-parameter: (String)
                ::: this parameter specifies the location and the filename of 
                the data which the header is to be extracted.
    """
    
    data = pd.read_csv(filename, usecols = (0,1), header = None,
                       names = ['Head1','Head2'])
    return (data.dropna(),)

#------------------------------------------------------------------------------
def dataload_range(basename, initial, final, outtype = 'pandas'):
    """
        The purpose of this function is to load the set of data into a tuple for
        for analysis.
            
            basename-parameter: (String)
                ::: The location of the file; since the filename is a standard
                output of the oscilloscope.
            
            initial-parameter: (Integer)
            ::: The file number which to begin the extraction.
            
            final-parameter: (Integer)
            ::: The file number which to end the extraction.
    """
    data = ()
    head = ()
    
    for i in range(initial, final + 1, 1):
        
        if digit_counter(i) == 1:
            filename = basename + 'TEK000' + str(i) + '.csv'
        
        elif digit_counter(i) == 2:
            filename = basename + 'TEK00' + str(i) + '.csv'
        
        elif digit_counter(i) == 3:
            filename = basename + 'TEK0' + str(i) + '.csv'
        
        else:
            filename = basename + 'TEK' + str(i) + '.csv'
        
        if outtype.lower() in ['pandas']:
            data = data + dataload_csv(filename)
            head = head + headerload_csv(filename)
        elif outtype.lower() in ['numpy']:
            data = data + dataload_csv(filename).values
            head = head + headerload_csv(filename)
        
    return data, head

#------------------------------------------------------------------------------
def digit_counter(integer):
    """
       The purpose of this code is to output the number of digits of the
       integer input.
           
           integer-parameter: (Integer)
           ::: the integer whose digits is needed.
   """    
    return int(np.log10(integer)) + 1

#------------------------------------------------------------------------------
def initial_2plot(data1, data2, transpose = False):
    """
        Basic pair-plot function; will likely not be extended. Because every 
        set of data needs a particular set of code.
            
            data1 and data2: (2-D numpy arrays)
            ::: The data which needs to be plotted; the initial_processdata
            function is called.
    """
    if transpose == True:
        
        dataA = initial_processdata(data1, transpose = True)
        dataB = initial_processdata(data2, transpose = True)
    else:
        dataA = initial_processdata(data1)
        dataB = initial_processdata(data2)
    
    
    fig = plt.figure(num = 2)
    
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    ax1.grid()
    ax2.grid()
    ax1.plot(dataA[0][1200:],dataA[1][1200:],'o')
    ax2.plot(dataB[0][1200:],dataB[1][1200:],'o')
    
    fig.show()    
    
    
#------------------------------------------------------------------------------
def initial_processdata(data, transpose = False):
    """
        This function outputs the noise subtracted data.
            
            data: (2-D numpy array)
            ::: The data which needs to be noise_reduced.
            
            transpose-parameter: (Boolean)
            ::: If set to True the output will be the noise reduced transpose 
            of the data.
            
    """
    if transpose == True:
        
        dataT = np.transpose(data)
        dataT_avg = np.average(np.abs(dataT[1][:1000]))
    
        dataT[1] = np.abs(dataT[1]) - dataT_avg
    
    else:
        
        dataT = data
        dataT_avg = np.average(np.abs(dataT[1][:1000]))
        
        dataT[1] = np.abs(data[1]) - dataT_avg
            
        
    return dataT
    
    
    
    
    
