import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the differential equation: dy/dt = -2y + 1
def model(y, t):
    # dydt = -2 * y + 1
    P = -1
    I = 0
    D = -1.8
    ext = 1
    dydt = np.array([
        # y'
        y[1],
        # y''
        P * y[0] + D * y[1] + ext            
    ])
    return dydt

# Initial condition: y(0) = 0
y0 = np.array([
    0,  # y
    0   # y'
])

# Time points at which to solve the ODE
t = np.linspace(0, 50, 1000)

# Solve the ODE
y = odeint(model, y0, t)

# Plot the solution
plt.plot(t, y[:,0], label='y(t)', color='b')
plt.title('Solution of dy/dt = -2y + 1')
plt.xlabel('Time (t)')
plt.ylabel('y(t)')
plt.legend()
plt.grid(True)
plt.show()
