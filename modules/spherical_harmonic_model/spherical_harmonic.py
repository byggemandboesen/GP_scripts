from scipy.special import legendre
import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import numpy as np

lat = np.linspace(-np.pi/2,np.pi/2,180)
lon = np.linspace(-np.pi,np.pi,180)
nlat = len(lat)
nlon = len(lon)

# Grid matrices
lat = np.column_stack((lat,)*nlon)
lon = np.column_stack((lon,)*nlat)

# Constants
r = 6378000
a = 6378000

# Grid to be filled with values
vals = np.zeros_like(lat)

def sphericalHarmonicModule():
    with dpg.collapsing_header(label = "Spherical harmonic model"):
        dpg.add_text("Simulate gravity with a spherical harmonic model")
        dpg.add_slider_int(label = "Degree", min_value=1, max_value=13, default_value = 13, tag = "spherical_degree")

        dpg.add_spacer(height=5)
        dpg.add_button(label = "Simulate", callback = simulate)


def simulate():
    degree = dpg.get_value("spherical_degree")
    print(f"Simulating with {degree} degrees")

    for i in range(nlat):
        term = np.zeros(nlon)

        # Not quite the Schmidt seminormalized Legendre polynomial but whatever
        legendre_coeff = legendre(i)
        P = 0
        x_val = np.cos(lat[i,0]+np.pi/2)
        
        # Calculate Legendre polynomial
        for j in range(i,0,-1):
            P += legendre_coeff[j]*x_val**j
        
        for m in range(i):
            q = 1

        

    # TODO - Dearpygui heat plot
