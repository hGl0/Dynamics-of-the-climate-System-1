import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

T0 = 0          # Ausgangstemp
tau1 = 30       # in Jahren
T2xco2 = 3.2    # wird sich angenähert
C0 = 280        # first value
T = [T0]
h = 1

df = pd.read_csv("rcp26.csv")
co = df['CO2']

def ocean(T):
    integral = 0
    for i in range(0, len(T)-1):
        integral = (integral + (T[i]-T[i-1])/np.sqrt((len(T)-1-i)))
    return integral

def ice_albedo(alpha):
    Ts = (2/(5.67*(10**(-8)))*(1-alpha)*340)**(1/4)-273.1
    return Ts

# alpha operates on global temperature => +15
#Stufen
def alpha1(Temp):
    if Temp <= -10:
        return 0.6
    if Temp <= 0:
        return 0.5
    if Temp <= 10:
        return 0.3
    if Temp <= 20:
        return 0.2
    else:
        return 0.1

# linear
def alpha2(Temp):
    if -10 <= Temp and Temp <= 20:
        return -0.012*Temp+0.48
    else:
        return alpha1(Temp)

# const
def alpha3(Temp):
    return 0.3

def myles_int(T, tau, T2xco2, co, C0, df, h):
    for i in range(0, len(df)-1):
        temp = T[i]+((1/tau)*T2xco2*np.log2(co[i]/C0)-(1/tau)*T[i])-h*ocean(T)+(ice_albedo(alpha1(15+T[i]))-ice_albedo(alpha1(15+T[i-1])))
        T.append(temp)
    return T

T1 = myles_int([T0], 30, T2xco2, co, C0, df, 0)
T2 = myles_int([T0], 30, T2xco2, co, C0, df, 1)
# a = myles_int([T0], 30, T2xco2, co, C0, df, h)[1]
plt.plot(df['YEARS'], T1, color="blue")
plt.plot(df['YEARS'], T2, color="orange")
# plt.plot(a, color="green")
plt.xlabel("Time [Jahre]")
plt.ylabel("Temperature [°C]")
plt.title("CO2 Data from RCP 2.6, C_0=280, T_2xco2 = 3.2")
plt.show()