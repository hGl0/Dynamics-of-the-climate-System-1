import numpy as np
import matplotlib.pylab as plt
import cmath as mth
import random as rd
import pandas as pd

I0 = 1350 # W/m2 solar insulation
pi = np.pi
Tabs0 = 273.15 # K
sigma = 5.67e-8 # Stefan-Boltzmann constant
bb_efficiency = 0.6 # black body efficiency

Kc = 3 # K climate sensitivity
C0 = 280 # ppm
alpha0 = 0.30581537 # 0.3
alpha_cold = 0.6
alpha_warm = 0.3
Talpha_treshhold = Tabs0+11 # C
Talpha_scale = 2 # K

taus = 1 # yr
tauc = 25 # yrs
taudo = 200 # yrs

hT = 1/np.sqrt(100) # 1/sqrt(yrs)
hE = 1/1000 #h emissions, temperature feedback


eps_aa = 0.1
eps_ml = 0.5
eps_do = 0.25

# numerical constant
dt = 1 # yr

# Function definitions
def Tsolar(alpha,t):
    val = (1-alpha)*((0.3*np.sin(t*0.01))+1.2)*I0/(4*sigma*bb_efficiency)
    val = pow(val,0.25)
    return val

def Tco2(C):
    val = Kc*np.log(C/C0)/np.log(2)
    return val

def alpha(T):
    val = alpha_cold + (alpha_warm - alpha_cold)/2*(1+np.tanh((T-Talpha_treshhold)/Talpha_scale))
    return val 

def Ocean_uptake(Tc):
        ocean_uptake = 0
        t = len(Tc)-1
        for t_dash in range(0,t):
            ocean_uptake = ocean_uptake+(Tc[t_dash]-Tc[t_dash-1])/np.sqrt(t-t_dash)
        return(ocean_uptake)


def C_ocean_uptake(Cml):
        ocean_uptake = 0
        t = len(Cml)-1
        for t_dash in range(0,t):
            ocean_uptake = ocean_uptake+(Cml[t_dash]-Cml[t_dash-1])/np.sqrt(t-t_dash)
        return(ocean_uptake)   

# Emission time series
Emissions = np.zeros([1500, 1])
#Emissions[10] = 100

#use rcp2.6 emissions for sanity check
# =============================================================================
#rcp26 = pd.read_csv('C:\\Users\\stecheme\\Documents\\RCP\\rcp26.csv')  
#C_rcp = rcp26['CO2']
#Emissions = np.diff(C_rcp)
# =============================================================================
def emissions(Emissions_in,T):
    E_new = Emissions_in+hE*(T-Tabs0)
    return(E_new)
    

# =============================================================================
# print(Tsolar(0.0))
# print(Tco2(140))
# print(len(Emissions))
# 
# =============================================================================
# variables
Ts = [] # surface temperature set by solar insulation
Tc = [] # surface temperature set by 
T = []
TCelcius = []

Caa = [] # C atmospheric accumulation
Cml = [] # C mixed layer
Cdo = [] # C deep ocean
C = [] # C 
alp = [] # alpha

# initialization
Ts_old = Tsolar(alpha0,0)
Tc_old = 0.0
T_old  = Ts_old + Tc_old
alpha_old = alpha(T_old)

Caa_old = 280.0 #C3
Cml_old = 0.0  #C1
Cdo_old = 0.0  #C2
C_old   = Caa_old + Cml_old + Cdo_old

for t in range(1,len(Emissions)):
    E = emissions(Emissions[t],T_old)
    
    Ts_new = Ts_old + dt * (Tsolar(alpha_old,t) - Ts_old/taus)
    Tc_new = Tc_old + dt * (Tco2(C_old)/tauc - Tc_old/tauc-hT*Ocean_uptake(Tc))
    T_new = Ts_new + Tc_new
    Caa_new = Caa_old + dt * (eps_aa*E)
    Cml_new = Cml_old + dt * (eps_ml*E-hT*C_ocean_uptake(Cml))
    Cdo_new = Cdo_old + dt * (eps_do*E - Cdo_old/taudo)
    C_new = Caa_new + Cml_new + Cdo_new

    alpha_new = alpha(T_new)
    
    # save
    Ts.append(Ts_new)
    Tc.append(Tc_new)
    T.append(T_new)
    TCelcius.append(T_new-Tabs0)
    Caa.append(Caa_new)
    Cml.append(Cml_new)
    Cdo.append(Cdo_new)
    C.append(C_new)
    alp.append(alpha_new)
    
    # update
    Ts_old = Ts_new
    Tc_old = Tc_new
    T_old = T_new
    Caa_old = Caa_new
    Cml_old = Cml_new
    Cdo_old = Cdo_new
    C_old = C_new
    alpha_old = alpha_new
    
plt.figure()
plt.plot(C)

plt.figure()
plt.plot(Ts)

plt.figure()
plt.plot(TCelcius)
plt.xlabel("Years")
plt.ylabel("Temperature (°C)")
plt.title("Temperature change dependent on periodic I0")

plt.figure()
plt.plot(alp)

print(alp[-1])

#atest = []
#Tint = np.linspace(-10,30,400)
#for i in range(len(Tint)):
#    val = alpha(Tabs0+Tint[i])
#    print(i,Tint[i],val)
#    atest.append(val)
