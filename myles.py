import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

T0 = 0          # Ausgangstemp
tau = 30       # in Jahren
T2xco2 = 3.2    # wird sich angenähert
C0 = 278         # first value

T = [T0]

df = pd.read_csv("rcp26.csv")
co = df['CO2']


for i in range(0,len(df)-1):
    temp = T[i]+((1/tau)*T2xco2*np.log2(co[i]/C0)-(1/tau)*T[i])
    T.append(temp)

#Plottet Daten
plt.plot(df['YEARS'], T)
plt.xlabel("Time [Jahre]")
plt.ylabel("Temperature [°C]")
plt.show()




