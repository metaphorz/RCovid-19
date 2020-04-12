#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
from scipy.special import erf
from scipy.optimize import fmin_bfgs

# Total population, N.
N = 40000000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.11, 1./15 
# A grid of time points (in days)
t = np.linspace(0, 600, 600)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S/10000, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/10000, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/10000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,100)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()

#Data Pre-processing for Italy
url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
df = pd.read_csv(url)
print(df.tail(1))
dfc = df.loc[:,['data','totale_casi','deceduti','tamponi']]
FMT = '%Y-%m-%d %H:%M:%S'
date = dfc['data']
dfc['data'] = date.map(lambda x : (datetime.strptime(x.replace('T',' ',1), FMT) - datetime.strptime("2020-01-01 00:00:00", FMT)).days  )
print(dfc.tail(1))

#Turkey Daily Rates
ytr=[191,359,670,947,1236,1529,1872,2433,3629,5698,7402,9217,10827,13531,15679,18315,20921,23934,27069,30217,34109,38226,42282,47029,52167]
dtr=[2,4,9,21,30,37,44,59,75,92,108,131,168,214,277,356,425,501,574,649, 725,812,908,1006,1101]
xtr=[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
ttr=[]

#Italy Daily Rates
xit = list(dfc.iloc[:,0])
yit = list(dfc.iloc[:,1])
dit = list(dfc.iloc[:,2])
tit = list(dfc.iloc[:,3])

def exponential_model(x,a,b,c):
    return a*np.exp(b*(x-c))

exp_fit_param_tr, exp_fit_cov_tr = curve_fit(exponential_model,xtr,ytr,p0=[0.7,0.7,0.7])
print("Exponential Model Params: ", exp_fit_param_tr)
print("Exponential Model Prediction For  Day: ",len(xtr)+7-1, " is ", exponential_model(len(xtr)-1+7,*exp_fit_param_tr))
print("Exponential Model Prediction For  Day: ",len(xtr)+7,   " is ", exponential_model(len(xtr)+7,*exp_fit_param_tr))
print("Exponential Model Prediction For  Day: ",len(xtr)+1+7, " is ", exponential_model(len(xtr)+1+7,*exp_fit_param_tr))

def logistic_model(x,a,b,c):
    return c/(1+np.exp(-1*a*(x-b)))

logistic_fit_param_tr, logistic_fit_cov_tr=curve_fit(logistic_model,xtr,ytr,p0=[1.0,1.0,30000])
print("Logistic Model Params: ", logistic_fit_param_tr)
print("Logistic Model Prediction For  Day: ",len(xtr)-1, " is ", logistic_model(len(xtr)-1,*logistic_fit_param_tr))
print("Logistic Model Prediction For  Day: ",len(xtr),   " is ", logistic_model(len(xtr),*logistic_fit_param_tr))
print("Logistic Model Prediction For  Day: ",len(xtr)+1, " is ", logistic_model(len(xtr)+1,*logistic_fit_param_tr))

def erf_model(x,a,b,c):
    return (c*(erf(a*(x-b))))/2

def erf_derivate(x,a,b,c):
     return ((a*c)*(2/np.pi)*np.exp(-1*(a*x-a*b)*(a*x-a*b)))

#x0=[1.0,3.0,50000]   

#xr=fmin_bfgs(erf_model,x0,erf_derivative,maxiter=10000)
#print(xopt)

#erf_fit_param_tr, erf_fit_cov_tr = curve_fit(erf_model,xtr,ytr,p0=[1e-1,0.5,20000])
#print("Erf Model Params: ", erf_fit_param_tr)
#print("Erf Model Prediction For  Day: ",len(xtr)-1+7, " is ", erf_model((len(xtr)-1+7),*erf_fit_param_tr))
#print("Erf Model Prediction For  Day: ",len(xtr)+7,   " is ", erf_model((len(xtr)+7),*erf_fit_param_tr))
#print("Erf Model Prediction For  Day: ",len(xtr)+1+7, " is ", erf_model((len(xtr)+1+7),*erf_fit_param_tr))

def stats(d,y):
    nrate=[]
    drate=[]
    for i in np.arange(len(y)-1):
         nrate.append((y[i+1]-y[i])/y[i]*100)
    for i in np.arange(len(y)):
         drate.append(d[i]/y[i]*100)
    return (nrate,drate)
nrateit,drateit = stats(dit,yit)
nratetr,dratetr = stats(dtr,ytr)
#print(nrateit)
#print(drateit)
#print(nratetr)
#print(dratetr)

fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(np.arange(len(nrateit)), nrateit, 'b', alpha=0.5, lw=2, label='Italy')
ax.plot(np.arange(len(nratetr)), nratetr, 'r', alpha=0.5, lw=2, label='Turkey')
#ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Relative Daily Increase')
ax.set_ylim(0,100)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
#
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(np.arange(len(drateit)), drateit, 'b', alpha=0.5, lw=2, label='Italy')
ax.plot(np.arange(len(dratetr)), dratetr, 'r', alpha=0.5, lw=2, label='Turkey')
#ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Fatality Rate')
ax.set_ylim(0,13)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
# Fatality rate over time
# Number of cases over time
# Number of tests over time
# Number of cases per 100K population
# Number of test per 100K population
# Number of hospitilization  
