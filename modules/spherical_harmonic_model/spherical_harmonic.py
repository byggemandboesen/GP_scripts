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
lon = np.transpose(np.column_stack((lon,)*nlat))

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
    
    with open("modules/spherical_harmonic_model/g_coefficients.txt", "r") as g_file:
        g_coeff = np.array([[float(val) for val in line.split()] for line in g_file])
    with open("modules/spherical_harmonic_model/h_coefficients.txt", "r") as h_file:
        h_coeff = np.array([[float(val) for val in line.split()] for line in h_file])

    # Not quite the Schmidt seminormalized Legendre polynomial but whatever
    legendre_poly = [legendre(i) for i in range(degree)]

    # TODO Fix simulation only working for 13 degrees

    # Loop over latitude
    for i in range(nlat):
        # Loop over degree
        for n in range(degree):
            term = np.zeros(nlon)
            
            # Calculate Legendre polynomial
            # NOTE The legendre polynomial is not Schmidt semi normalized like the Matlab simulation is!
            # Tbh I'm not quite sure what the difference may be
            x_val = np.cos(lat[i,0]+np.pi/2)
            P = np.sum([coeff*x_val**(n-f) for f, coeff in enumerate(legendre_poly[n])])
            
            # Loop over order
            for m in range(n):
                term += P * ((g_coeff[n,m]*np.cos(m*lon[i,])) + (h_coeff[n,m]*np.sin(m*lon[i,])))

            vals[i,] += term * (n+1)*(a/r)**(n+2)

    
    # TODO
    # Try to update current plot if one exists, otherwise create one
    
    # Create axis labels    
    lon_labels = tuple(zip(*(tuple(np.linspace(-180, 180, 11, dtype=str)), tuple([i/10 for i in range(11)]))))
    lat_labels = tuple(zip(*(tuple(np.linspace(-90, 90, 11, dtype=str)), tuple([i/10 for i in range(11)]))))
    # print(lon_labels)
    
    with dpg.window(label = "Simulation", tag = "b_field_sim_window", width=500, height=500,on_close=dpg.delete_item):

        with dpg.group(horizontal=True):
            dpg.add_colormap_scale(min_scale=np.min(vals), max_scale=np.max(vals), width = 90, height=-1)
            dpg.bind_colormap(dpg.last_item(), dpg.mvPlotColormap_Jet)
            with dpg.plot(label = "Spherical harmonic B-field simulation", width=-1,height=-1, tag = "b_field_plot"):
                dpg.bind_colormap("b_field_plot", dpg.mvPlotColormap_Jet)
                
                # Create axis and update their ticks
                dpg.add_plot_axis(dpg.mvXAxis, label = "Longitude") # , lock_max=True, lock_min=True
                dpg.set_axis_ticks(dpg.last_item(), lon_labels)
                dpg.add_plot_axis(dpg.mvYAxis, label = "Latitude", tag = "y_axis_bfield") # , lock_max=True, lock_min=True
                dpg.set_axis_ticks(dpg.last_item(), lat_labels)
                
                # And then add data to plot
                dpg.add_heat_series(vals, nlat, nlon, parent="y_axis_bfield", scale_max=np.max(vals), scale_min=np.min(vals), format ="", tag = "heatmap")


