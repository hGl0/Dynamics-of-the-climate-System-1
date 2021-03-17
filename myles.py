import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

T0 = 0          # Ausgangstemp
tau1 = 30       # in Jahren
T2xco2 = 3.2    # wird sich angenähert
C0 = 280        # first value
T = [T0]

df = pd.read_csv("rcp26.csv")
co = df['CO2']

def myles(T, tau, T2xco2, co, C0, df):
    for i in range(0, len(df)-1):
        temp = T[i]+((1/tau)*T2xco2*np.log2(co[i]/C0)-(1/tau)*T[i])
        T.append(temp)
    return T

T1 = myles([T0], 10, T2xco2, co, C0, df)
T2 = myles([T0], 20, T2xco2, co, C0, df)
T3 = myles([T0], 30, T2xco2, co, C0, df)
T5 = myles([T0], 50, T2xco2, co, C0, df)
T10 = myles([T0], 100, T2xco2, co, C0, df)
T20 = myles([T0], 200, T2xco2, co, C0, df)
#Plottet Daten
plt.plot(df['YEARS'], T1, label="Tau = 10")
plt.plot(df['YEARS'], T2, label="Tau = 20")
plt.plot(df['YEARS'], T3, label="Tau = 30")
plt.plot(df['YEARS'], T5, label="Tau = 50")
plt.plot(df['YEARS'], T10, label="Tau = 100")
plt.plot(df['YEARS'], T20, label="Tau = 200")
plt.xlabel("Time [Jahre]")
plt.ylabel("Temperature [°C]")
plt.legend()
plt.title("CO2 Data from RCP 2.6, C_0=280, T_2xco2 = 3.2")
plt.show()




