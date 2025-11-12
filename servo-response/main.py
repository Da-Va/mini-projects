import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# PID constants
P = -1
I = -0
D = -1.9

M = 1.0

t_span = (-0,50)
t_max_step = 0.01

# External force
def ext(t):
    q = .0
    # ext =  1 - (1/q**2)*(t - q)**2 if t < q else 1 if t >= 0 else 0
    # ext =  1 #if 0 <= t <= 0.5 else 0 # or 1 <= t <= 1.5 else 0
    ext = 1#min(t, 1)
    return ext

# Define the differential equation: dy/dt
def model(t, y):
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
    0,  # y'
    0   # int y dt
])

# Solve the ODE
solution = solve_ivp(model, t_span, y0, max_step=t_max_step)
y = solution.y.T
t = solution.t

# Extracted data
y_d = np.array([ model(t, y) for t,y in zip(t, y) ])
p_gain_estim = -P * y[:,0]
pid_gain = -P * y[:,0] - D * y[:,1] - I * y[:,2] #+ y_d[:,1]
p_gain = -P * y[:,0]
d_gain = -D * y[:,1]
F_ext = np.array([ext(t) for t in t])

# Plot data
plt.plot(t, y[:,0], label='y(t)', color='teal')
plt.plot(t, y[:,1], label='y\'(t)', color='r')
plt.plot(t, y_d[:,1], label='y\'\'(t)', color='g')
plt.plot(t, pid_gain, label='pid_gain(t)', color='purple')
# plt.plot(t, pid_gain+M*acc_estim, label='pid_gain(t) + M*acc_sctim', color='teal')
plt.plot(t, p_gain, label='Py(t)', color='y')
# plt.plot(t, d_gain, label='Dy\'(t)', color='pink')
plt.plot(t, F_ext, label='F_ext', color='black')
plt.xlabel('Time (t)')
plt.ylabel('y(t) et al.')
plt.legend()
plt.grid(True)
plt.show()