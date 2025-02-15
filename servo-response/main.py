import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# PID constants
P = -100
I = -0
D = -20

T = 2

def ext(t):
    # ext = 1
    q = 0.3
    ext =  1 - (1/q**2)*(t - q)**2 if t < q else 1
    # ext = 1/(1+math.e**(-(t-3)*8))
    # ext =  2*t if t < 0.5 else 1
    # ext = np.sin(0.1*t) + 0.1*np.sin(t) + np.sin(2 * t)
    # ext = 1 if (t < 2) else 0
    return ext

# Define the differential equation: dy/dt
def model(y, t):
    dydt = np.array([
    # y'
        y[1],
    # y''
        P * y[0] + D * y[1] + I * y[2] + ext(t),
    # int y dt
        y[0]
    ])
    return dydt

# Initial condition: y(0)
y0 = np.array([
    0,  # y
    0,   # y'
    0   # int y dt
])

# Time points at which to solve the ODE
t = np.linspace(0, T, 1000)

# Solve the ODE
y = odeint(model, y0, t)

y_d = np.array([ model(y, t) for y,t in zip(y, t) ])
p_gain_estim = -P * y[:,0]
pid_gain = -P * y[:,0] - D * y[:,1] - I * y[:,2]

F_ext = np.array([ext(t) for t in t])

# Plot the solution
plt.plot(t, 10*y[:,0], label='10y(t)', color='b')
plt.plot(t, y[:,0], label='y(t)', color='teal')
plt.plot(t, y[:,1], label='y\'(t)', color='r')
plt.plot(t, y_d[:,1], label='y\'\'(t)', color='g')
plt.plot(t, pid_gain, label='pid_gain(t)', color='purple')
plt.plot(t, F_ext, label='F_ext', color='black')
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()
