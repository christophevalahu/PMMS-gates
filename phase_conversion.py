from math import sin, sqrt, cos, pi, atan2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

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

def norm_vect_dist(R, c) :
    return R*sqrt(1 - (c**2)/(4*R**2))

def centerCircle(x1, y1, x2, y2, arc_l, R) :
    
    seg_l = sqrt((x1-x2)**2 + (y1-y2)**2)
    
    norm_vect_d = norm_vect_dist(R, seg_l)
    
    mid_seg_point_x = (x1 + x2)/2
    mid_seg_point_y = (y1 + y2)/2
    
    norm_vec_x = -(y2 - y1)
    norm_vec_y = (x2 - x1)
    l_norm_vec = sqrt(norm_vec_y**2 + norm_vec_x**2)
    
    norm_vec_y = norm_vec_y/l_norm_vec
    norm_vec_x = norm_vec_x/l_norm_vec
    
    circ_x = mid_seg_point_x + norm_vec_x * norm_vect_d
    circ_y = mid_seg_point_y + norm_vec_y * norm_vect_d
    
    return circ_x, circ_y

def tanAngle(circ_x0, circ_y0, x1, y1, x2, y2) :
    
    dx1 = x1 - circ_x0
    dy1 = y1 - circ_y0
    dx2 = x2 - circ_x0
    dy2 = y2 - circ_y0
        
    if abs(dy1) < 1e-10 :
        if -dx1 >= 0: theta1 = -pi/2
        else: theta1 = pi/2
    else :
        theta1 = atan2(dx1, -dy1)
        
    if abs(dy2) < 1e-10 :
        if -dx2 >= 0: theta2 = -pi/2
        else: theta2 = pi/2
    else :
        theta2 = atan2(dx2, -dy2)
        
    return [theta1, theta2]

def convertAngles(thetas, delta) :
    
    
    phis = np.empty(len(thetas), dtype=object)
    dphis = np.empty(len(thetas) - 1, dtype=object)

    R = 2*pi/delta
    Nsegs = len(thetas)
    
    l_arc = 2*pi*R/Nsegs
    l_seg = 2*R*sin(l_arc/(2*R))
    
    x1 = 0
    y1 = 0
    x2 = cos(thetas[0]) * l_seg + x1
    y2 = sin(thetas[0]) * l_seg + y1

    [circx, circy] = centerCircle(x1, y1, x2, y2, l_arc, R)
    [phi11, phi12] = tanAngle(circx, circy, x1, y1, x2, y2)

    phis[0] = phi11

    x1 = x2
    y1 = y2

    x1 = 0
    y1 = 0

    for i in range(len(thetas) - 2) :
    # Find three sets of coordinates for 2 consecutive vectors
    
        theta0 = thetas[i]
        theta1 = thetas[i+1]

        x2 = cos(theta0) * l_seg + x1
        y2 = sin(theta0) * l_seg + y1

        x3 = x2 + cos(theta1) * l_seg 
        y3 = y2 + sin(theta1) * l_seg 

        [circx, circy] = centerCircle(x1, y1, x2, y2, l_arc, R)
        [phi11, phi12] = tanAngle(circx, circy, x1, y1, x2, y2)


        [circx2, circy2] = centerCircle(x2, y2, x3, y3, l_arc, R)
        [phi21, phi22] = tanAngle(circx2, circy2, x2, y2, x3, y3)

        x1 = x2
        y1 = y2

        phis[i+1] = phis [i] + ((phi21 - phi12) % (2*pi))
 
    
    return phis
