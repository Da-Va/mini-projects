import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# PID constants
P = -100
I = -0
D = -20

t0 = 0
T = 3
M = 1.0

def ext(t):
    ext = 1
    q = 0.1
    ext =  1 - (1/q**2)*(t - q)**2 if t < q else 1 if t > 0 else 0
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
        (P * y[0] + D * y[1] + I * y[2] + ext(t))/M,
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
t = np.linspace(t0, T, 1000)

# Solve the ODE
y = odeint(model, y0, t)

y_d = np.array([ model(y, t) for y,t in zip(y, t) ])
p_gain_estim = -P * y[:,0]
pid_gain = -P * y[:,0] - D * y[:,1] - I * y[:,2] #+ y_d[:,1]
s = max(1, int(0.02/(t[1]-t[0])))
acc_estim = np.array([ (y[i,1] - y[i-s,1] if i > s else y[i,1])/(s*(t[1]-t[0])) for i in range(t.size) ])
p_gain = -P * y[:,0]
d_gain = -D * y[:,1]

F_ext = np.array([ext(t) for t in t])

# Plot the solution
plt.plot(t, 10*y[:,0], label='10y(t)', color='b')
plt.plot(t, y[:,0], label='y(t)', color='teal')
plt.plot(t, y[:,1], label='y\'(t)', color='r')
plt.plot(t, y_d[:,1], label='y\'\'(t)', color='g')
plt.plot(t, pid_gain, label='pid_gain(t)', color='purple')
plt.plot(t, pid_gain+M*acc_estim, label='pid_gain(t) + M*acc_sctim', color='teal')
# plt.plot(t, acc_estim, label='acc_estim', color='purple')
plt.plot(t, p_gain, label='Py(t)', color='y')
plt.plot(t, d_gain, label='Dy\'(t)', color='pink')
plt.plot(t, F_ext, label='F_ext', color='black')
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()
