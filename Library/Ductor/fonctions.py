import math
import numpy as np
from scipy.optimize import fsolve

#constant
AIRDENSITY = 1.23 # kg/m3
AIRVISCOSITY = 1.79e-5 #Ns/m2 (dynamique)
GALVANISEDROUGHNESS = 0.15 #mm


# Colebrook-White equation to solve for Darcy friction factor (f)
def colebrook_white_equation(f, Re, epsilon_D):
    left_side = -2 * np.log10((epsilon_D / 3.7) + (2.51 / (Re * np.sqrt(f))))
    right_side = 1 / np.sqrt(f)
    return left_side - right_side

# Function to calculate Darcy friction factor (f) using Colebrook-White equation
def colebrook_white_friction_factor(Re, epsilon_D):
    f_guess = 0.02  # Initial guess for f
    f_solution = fsolve(colebrook_white_equation, f_guess, args=(Re, epsilon_D))
    return f_solution[0]

def darcy_weisbach(length,vel,diameter,f):
    pressure_loss = f*(length/diameter)*(AIRDENSITY * vel**2 / 2)
    return pressure_loss #N/m2

def duct_vel(diam, cfm):
    #diam unit: mm
    area = (math.pi*(diam/1000)**2)/4 #m^2
    vel = cfm/(area*10.76) #pieds minutes
    
    return vel

def pressure_loss(diameter, length, flow_rate):
    #  flow unit: cfm
    vel = duct_vel(diameter,flow_rate) #pieds min
    re = vel*0.00508*diameter/1000*AIRDENSITY/AIRVISCOSITY
    if re < 4000:
        HL_tot = 0
    else:       
        rr = GALVANISEDROUGHNESS/diameter
        f = colebrook_white_friction_factor(re, rr)
        HL_tot = darcy_weisbach(length, vel*0.00508, diameter/1000, f)
    
    return HL_tot #Pa

def headloss_air_MLCoeff(K,diam, cfm):
    dP = (K*1.2*(duct_vel(diam,cfm)*0.00508)**2)/2
    return dP #Pa