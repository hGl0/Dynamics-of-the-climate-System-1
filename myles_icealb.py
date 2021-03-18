import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as random

rcp26 = pd.read_csv("rcp26.csv")
rcp45 = pd.read_csv('rcp45.csv')
rcp60 = pd.read_csv('rcp60.csv')
rcp85 = pd.read_csv('rcp85.csv')

co = rcp26['CO2']
T_init = 15
T0 = 0          # Ausgangstemp
tau = 30        # in Jahren
tau2 = 1000
T2xco2 = 3.2    # wird sich angenähert
C0 = 280        # first value
T = [T0]
h = 0.1
I0 = 340
bolz = 5.67 * 10**(-8)

def ocean(T):
    integral = 0
    for i in range(0, len(T)-1):
        integral = (integral + (T[i]-T[i-1])/np.sqrt((len(T)-1-i)))
    return integral

def ice_albedo(T, t):
    Ts = (2/bolz*(1-alpha(T))*(np.sin(t*0.01)+1)*I0)**(1/4)-273.1
    return Ts

# alpha operates on global temperature => +T_init
# linear
def alpha(Temp):
    Temp += T_init
    if Temp >= -10 and Temp <= 20:
        return -1/60*Temp+8/15
    if Temp < -10:
        return 0.7
    if Temp > 20:
        return 0.2


def myles(T, co, h, a):
    for i in range(0, len(co)-1):
        if T[i] <= 0:
            tau2 = 10000
        if T[i] > 0:
            tau2 = 1000
        temp = T[i]+((1/tau)*T2xco2*np.log2((co[i])/C0)-(1/tau)*T[i])-h*ocean(T) + a*(1/tau2)*(ice_albedo(T[i], i) - Ts_ref)
        T.append(temp)
    return T

Ts_ref = 29.69

def glacial_carbon(E):
    co2 = [E]
    for i in range(0, 15000):
        co2.append(co2[i]+0.75*2-1/200*(co2[i])-h*ocean(co2))
    return co2

def carbon_rcp(E):
    co2 = [E]
    for i in range(0, 735):
        co2.append(co2[i]+(0.75*(co[i+1]-co[i])*10-1/200*(co2[i])-h*ocean(co2)))
    return co2


c_glac = glacial_carbon(C0)
c_rcp = carbon_rcp(C0)
'''
no_ocean = myles([T0], c_rcp, 0, 0)
ocean_only = myles([T0], c_rcp, h, 0)
ocean_ice = myles([T0], c_rcp, h, 1)
ocean_ice_co = myles([T0], c_rcp, h, 1)
ocean_ice_corcp = myles([T0], c_rcp, h, 1)
'''
glacial = myles([T0], c_glac, h, 1)


#plt.plot(rcp26.YEARS[:700], no_ocean[:700], color="blue")
#plt.plot(rcp26.YEARS[:700], ocean_only[:700], color="orange")
#plt.plot(rcp26.YEARS[:700], ocean_ice[:700], color="green")#
#plt.plot(rcp26.YEARS[:700], ocean_ice_co[:700], color="red")
#plt.plot(rcp26.YEARS[:700], ocean_ice_corcp[:700], color="red")
plt.plot(glacial)
#plt.plot(c, color="orange")
#plt.plot(c_rcp, color="blue")
# plt.plot(a, color="green")
plt.show()