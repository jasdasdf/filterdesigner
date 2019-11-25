# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:05:23 2019

@author: Yuki-F
"""

import scipy.signal as signal
import scipy as sp
import numpy as np

def impz(system):
    """
    Impulse response of a digital filter.
    
    Parameters
    ----------
        system : an instance of the LTI class or a tuple of array_like
            describing the system.
            The following gives the number of elements in the tuple and
            the interpretation:
                
                * 1 (instance of `lti`)
                * 2 (num, den)
            
    Returns
    -------
        T : ndarray
            A 1-D array of time points.
            
        yout : ndarray
            A 1-D array containing the impulse response of the system (except
            for singularities at zero).
            
    Notes
    -----
        If (num, den) is passed in for ``system``, coefficients for both the
        numerator and denominator should be specified in describing exponent
        order (e.g. ``s^2 + 3s + 5`` would be represented as ``[1, 3, 5]``).
    """
    
    if type(system[1]) == int and system[1] == 1:
        # FIR filter
        return np.array(range(len(b))), b
    
    elif type(system[1]) == np.ndarray:
        # IIR filter 
        return signal.impulse(system)
    
    else:
        raise ValueError
        
def freqz(system, worN=512, fs=2*np.pi, outform = 'complex'):
    """
    Frequency response of a digital filter.
    
    Parameters
    ----------
        system : an instance of the LTI class or a tuple of array_like
            describing the system.
            The following gives the number of elements in the tuple and
            the interpretation:
                
                * 1 (instance of `lti`)
                * 2 (num, den)
                
        worN : {None, int, array_like}, optional
            If a single integer, then compute at that many frequencies 
            (default is N=512). This is a convenient alternative to:

                np.linspace(0, fs if whole else fs/2, N, endpoint=False)
            
            Using a number that is fast for FFT computations can result in 
            faster computations (see Notes).
            If an array_like, compute the response at the frequencies given. 
            These are in the same units as fs.
            
        fs : float, optional
            The sampling frequency of the digital system.
            Defaults to 2*pi radians/sample (so w is from 0 to pi).
        
        
    Returns
    -------
        w : ndarray
            The frequencies at which h was computed, in the same units as fs.
            By default, w is normalized to the range [0, pi) (radians/sample).
                
        h : ndarray
            The frequency response, as complex numbers.
    """
    
    #周波数特性を計算
    w, h = signal.freqz(system[0], system[1], worN=worN, fs=fs)
    
    if outform == 'complex':
        #complexの場合，周波数特性を複素数で返す
        return w, h
    
    elif outform == 'dB':
        #dBの場合，周波数特性をdBの数値（20*np.log10(np.abs(h))）を返す
        h = 20 * np.log10(np.abs(h))
        return w, h
    
    elif outform == 'abs':
        #absの場合，周波数特性を複素数の絶対値（np.abs(h)）で返す
        h = np.abs(h)
        return w, h
    
    else:
        #それ以外では例外をスローする
        raise ValueError("Parameter outform is must be 'complex', 'dB', or"
                         +"'abs'.")

def grpdelay(system, worN=512, fs=2*np.pi):
    """
    Group delay of a digital filter.
    
    Parameters
    ----------
        system : an instance of the LTI class or a tuple of array_like
            describing the system.
            The following gives the number of elements in the tuple and
            the interpretation:
                
                * 1 (instance of `lti`)
                * 2 (num, den)
                
        worN : {None, int, array_like}, optional
            If a single integer, then compute at that many frequencies 
            (default is N=512). This is a convenient alternative to:

                np.linspace(0, fs if whole else fs/2, N, endpoint=False)
            
            Using a number that is fast for FFT computations can result in 
            faster computations (see Notes).
            If an array_like, compute the response at the frequencies given. 
            These are in the same units as fs.
            
        fs : float, optional
            The sampling frequency of the digital system.
            Defaults to 2*pi radians/sample (so w is from 0 to pi).
            
    Returns
    -------
        w : ndarray
            The frequencies at which h was computed, in the same units as fs.
            By default, w is normalized to the range [0, pi) (radians/sample).
            
        gd : ndarray
            The group delay.
    """
    
    #デジタルフィルタの群遅延を計算
    w, gd = signal.group_delay(system, w = worN, fs = fs)
    
    #計算誤差を整数に丸める
    gd = np.round(gd)
    
    #周波数と対応する群遅延を返す
    return w, gd
    
def phasez(system, worN = 512, fs = 2*np.pi, deg=False):
    """
    Group delay of a digital filter.
    
    Parameters
    ----------
        system : an instance of the LTI class or a tuple of array_like
            describing the system.
            The following gives the number of elements in the tuple and
            the interpretation:
                
                * 1 (instance of `lti`)
                * 2 (num, den)
                
        worN : {None, int, array_like}, optional
            If a single integer, then compute at that many frequencies 
            (default is N=512). This is a convenient alternative to:

                np.linspace(0, fs if whole else fs/2, N, endpoint=False)
            
            Using a number that is fast for FFT computations can result in 
            faster computations (see Notes).
            If an array_like, compute the response at the frequencies given. 
            These are in the same units as fs.
            
        fs : float, optional
            The sampling frequency of the digital system.
            Defaults to 2*pi radians/sample (so w is from 0 to pi).
            
        deg : boolean, optional
            If True, the phase response is returned as degree.
            Default is False.
            
    Returns
    -------
        w : ndarray
            The frequencies at which h was computed, in the same units as fs.
            By default, w is normalized to the range [0, pi) (radians/sample).
            
        phase : ndarray
            The phase response.
    """
    
    w, h = freqz(system, worN = worN, fs = fs)
    phase = sp.unwrap(sp.angle(h))
    
    if deg == True:
        phase = np.rad2deg(phase)
    
    return w, phase
    
if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    
    b, a = signal.iirdesign(0.715, 0.99, 1, 120)
    #b = signal.firwin(257, 21000/22050)
    #a = 1
    
    plt.figure()
    T, yout = impz((b, a))
    plt.plot(T, yout)
    plt.xlabel('Sample')
    plt.ylabel('Normalized Amplitude')
    
    plt.figure()
    w, h = freqz((b, a), fs = 44100, outform='dB')
    plt.plot(w, h)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude [dB]')
    
    plt.figure()
    w, gd = grpdelay((b, a), fs = 44100)
    plt.plot(w, gd)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Group delay [samples]')
    
    plt.figure()
    w, phase = phasez((b, a), fs = 44100)
    plt.plot(w, phase)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Phase [rad]')