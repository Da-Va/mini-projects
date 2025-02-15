import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# PID constants
P = -100
I = 0
D = -15

# Define the differential equation: dy/dt
def model(y, t):
    ext = 1
    # ext =  1 - (t - 1)**2 if t < 1 else 1
    ext *= 0.01
    dydt = np.array([
    # y'
        y[1],
    # y''
        P * y[0] + D * y[1] + ext            
    ])
    return dydt

# Initial condition: y(0)
y0 = np.array([
    0,  # y
    0   # y'
])

# Time points at which to solve the ODE
t = np.linspace(0, 2, 1000)

# Solve the ODE
y = odeint(model, y0, t)

y_d = np.array([ model(y, t) for y,t in zip(y, t) ])
p_gain = P * y[:,0]

# Plot the solution
plt.plot(t, y[:,0], label='y(t)', color='b')
plt.plot(t, y[:,1], label='y\'(t)', color='r')
plt.plot(t, y_d[:,1], label='y\'\'(t)', color='g')
plt.plot(t, p_gain, label='p_gain(t)', color='y')
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()
