from math import sin, sqrt, cos, pi, atan2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

def twotoneX(t) :
    # Returns x position of 2 tone MS phase space trajectory :
    # Re(a(t))
    # Input : Float
    return sin(2*t)/(4*sqrt(3)) - sin(4*t)/(4*sqrt(3))
    
def twotoneXlist(t) :
    # Returns x position of 2 tone MS phase space trajectory :
    # Re(a(t))
    # Input : List
    return [sin(2*t_i)/(4*sqrt(3)) - sin(4*t_i)/(4*sqrt(3)) for t_i in t]

def twotoneY(t) :
    # Returns y position of 2 tone MS phase space trajectory :
    # Im(a(t))
    # Input : Float
    return (1-cos(2*t))/(4*sqrt(3)) - (1-cos(4*t))/(4*sqrt(3))
   
def twotoneYlist(t) :
    # Returns y position of 2 tone MS phase space trajectory :
    # Im(a(t))
    # Input : List
    return [(1-cos(2*t_i))/(4*sqrt(3)) - (1-cos(4*t_i))/(4*sqrt(3)) for t_i in t]
    
    def circleFunc(t, x0, y0, r):
    return (twotoneX(t)-x0)**2 + (twotoneY(t) - y0)**2 - r**2

def sampleTimes(len_vec, N) :
    # Sample N equidistant times along the trajectory a(t)
    # by fiding successive crossings with circles. 
    times = np.empty(N, dtype=object)
    
    for i in range(N) :
        if i > 0:
            initial_guess = times[i-1]
            x0 = twotoneX(times[i-1])
            y0 = twotoneY(times[i-1])
        else :
            initial_guess = 0
            x0 = 0
            y0 = 0

        result = least_squares(lambda t:circleFunc(t, x0, y0, len_vec), (initial_guess+len_vec), bounds = ((i*len_vec), (2*pi)))

        times[i] = result.x[0]
    
    times = np.insert(times, 0, 0, axis = 0)
    
    return times

def timeObjFunc(len_vec, N) :
    times = sampleTimes(len_vec, N)
    return times[-1]

def optimizeSampleLen(N, tgate) :
    # Optimize the circle radius (= sample distance)
    ini_len_vec = pi/(2*N)
    
    result = least_squares(lambda l: abs(timeObjFunc(l, N)-tgate), (ini_len_vec), bounds = ((0),(pi)))
    return result.x[0]
    
def findVectAngles(times) :
    
    N = len(times)
    thetas = np.empty(N, dtype=object)
    
    for i in range(N - 1):

        x0 = twotoneX(times[i+1]) - twotoneX(times[i])
        y0 = twotoneY(times[i+1]) - twotoneY(times[i])
        
        thetas[i] = atan2(y0, x0) % (2*pi)
    
    return thetas

def thetaPM(t, theta_list) :
    N = len(theta_list)
    t_chunk = pi/N
    return np.piecewise(t, [((t >= i * t_chunk) & (t < (i+1) *t_chunk)) for i in range(N-1)], [theta_list[i] for i in range(N)])

def plotAngles(theta_list) :
    
    timesList = np.arange(0., pi, pi/1000)
    plt.plot(timesList, thetaPM(timesList, theta_list), 'r--')
    plt.xlabel("time [s]")
    plt.ylabel("phase [rad]")
    plt.show()
    
def plotSampleTimes(sample_times) :
    
    times_data = np.arange(0., pi, pi/1000)
    plt.plot(twotoneXlist(times_data), twotoneYlist(times_data), 'r--')
    plt.scatter(twotoneXlist(sample_times), twotoneYlist(sample_times), color = 'b')
    plt.show()

  
