# This is a simple Root Locus ploter for SISO transfer functions.
# Created by Derek Black

# Imports
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import polynomial as P
from sympy import *
from sympy import poly
from sympy import root

# Define Transfer Function's numerator and denominator coefficients
s = symbols('s')

# User input prompts
print("\n")
print("Welcome to the command line driven root locus plotter \n")
print("Use the variable 's' when entering your polynomials \n")
print("Enter your polynomials in the following format: \n")
print("s**2 + 2*s + 4, use '**' for powers \n")

# Collect transfer function from user
numerator = raw_input("Enter the Numerator Polynomial of Transfer Fucntion: \n")
denominator = raw_input("Enter the Denominator Polynomial of Transfer Fucntion: \n")

# Convert user's transfer function to symbolic polynomial
num_poly = poly(numerator)
den_poly = poly(denominator)

# Gather initial Poles and Zeros of static system
static_poles = num_poly.all_coeffs()
static_zeros = den_poly.all_coeffs()
static_poles = np.roots(static_poles)
static_zeros = np.roots(static_zeros)

# Specify the resolution of the Root Locus plot
# These are good settings to use if your own resolution settings don't work
length = 10000
gain_resolution = 0.001


# Set up initial conditions and empty arrays
k = 0
poles = []

for i in range(length):
    k = k + gain_resolution # Iterates through different gains of the system
    new_num_poly = num_poly*k
    cltf = new_num_poly.add(den_poly) # 1 + K*G(s)
    coeff = cltf.all_coeffs() # Gather all coefficients of new polynomial
    poles.append(np.roots(coeff)) 

# Convert poles list to numpy array for plotting
poles = np.concatenate(poles, axis=0)

# Plot Zooming
def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print event.button
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun


# Scatter plot of Root Locus
fig, ax = plt.subplots()
ax.grid(True)
ax.axhline(y=0, color='k')
ax.axvline(x=0, color='k')
ax.scatter(poles.real,poles.imag, color='black',s=0.5)
ax.scatter(static_poles.real,static_poles.imag,marker="o",s=80)
ax.scatter(static_zeros.real,static_zeros.imag,marker="x",s=80)
ax.set_title('Root Locus')
ax.set_xlabel('Real Axis (1/sec)')
ax.set_ylabel('Imaginary Axis (1/sec)')
scale = 1.5
f = zoom_factory(ax,base_scale = scale)
plt.show()

