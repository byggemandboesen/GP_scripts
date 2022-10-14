import json, os
import numpy as np
import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt

from modules.grav_anomaly.anomaly import Anomaly

def gravityAnomalyWindow():
    with dpg.collapsing_header(label = "Gravity anomalies"):
        dpg.add_text("Add, remove or simulate anomalies")
        print("Listing anomalies")


        # Table with added anomalies
        with dpg.tree_node(label = "Anomalies"):
            anomalies = getAnomalies()
            
            # Create table
            with dpg.table(tag="anomaly_table", header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, resizable=True):
                dpg.add_table_column(label = "Anomaly")
                dpg.add_table_column(label = "x-position")
                dpg.add_table_column(label = "Dimensions [x,y,z]")
                dpg.add_table_column(label = "Density diff.")
                dpg.add_table_column(label = "Depth")

                for i in range(len(anomalies)):
                    values = [i+1, anomalies[i].x_pos,anomalies[i].dim,anomalies[i].drho,anomalies[i].depth]
                    with dpg.table_row(tag=f"row{i}"):
                        for j in range(len(values)):
                            dpg.add_text(values[j])
        
        # Add anomalies
        with dpg.tree_node(label = "Add anomalies"):

            dpg.add_input_float(label="x position", default_value=0, tag="x_pos")
            
            dpg.add_text("Dimensions")
            with dpg.group(horizontal=True):
                dpg.add_input_float(label="x", default_value=100, tag = "x_dim", width=100)
                dpg.add_input_float(label="y", default_value=100, tag = "y_dim", width=100)
                dpg.add_input_float(label="z", default_value=100, tag = "z_dim", width=100)

            dpg.add_input_float(label = "Density diff.", default_value= 500, tag = "drho")
            dpg.add_input_float(label = "Depth", default_value=1000, tag = "depth")

            dpg.add_spacer(height=5)
            dpg.add_button(label = "Add", callback=addAnomaly)
        
        # Remove anomalies
        with dpg.tree_node(label = "Remove anomalies"):
            dropdown_values = [f"Anomaly {i+1}" for i in range(len(getAnomalies()))]
            dpg.add_combo(dropdown_values, label = "Select anomaly", width=200, tag="anomaly_to_remove")
            
            dpg.add_spacer(height=5)
            dpg.add_button(label = "Remove", callback=removeAnomaly)


        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_input_float(label = "x-min", tag = "x_min", width = 125, default_value=-20000)
            dpg.add_input_float(label = "x-max", tag = "x_max", width = 125, default_value=20000)

        dpg.add_button(label = "Simulate",callback=updatePlot)


def getAnomalies():
    '''
    Returns a list of anomaly objects
    '''
    print("Getting anomalies...")
    with open("modules/grav_anomaly/anomalies.json", "r") as anomaly_file:
        parsed = json.load(anomaly_file)
        n_anomalies = len(parsed)
        anomalies = [Anomaly]*n_anomalies
        
        # Create list of anomaly objects
        for i in range(n_anomalies):
            x_pos = float(parsed[i]["x_pos"])
            dim = list(parsed[i]["dim"])
            drho = float(parsed[i]["drho"])
            depth = float(parsed[i]["depth"])
            anomalies[i] = Anomaly(x_pos, dim, drho, depth)
    
    return anomalies


def addAnomaly():
    print("Adding anomaly...")

    anomaly_to_add = {
        "x_pos": dpg.get_value("x_pos"),
        "dim": [dpg.get_value("x_dim"),dpg.get_value("y_dim"),dpg.get_value("z_dim")],
        "drho": dpg.get_value("drho"),
        "depth": dpg.get_value("depth")
    }

    with open("modules/grav_anomaly/anomalies.json", "r+") as anomaly_file:
        parsed = json.load(anomaly_file)
        parsed.append(anomaly_to_add)

        anomaly_file.seek(0)
        json.dump(parsed, anomaly_file, indent = 4)
        anomaly_file.close()
    
    updateCurrentAnomalies()


def removeAnomaly():
    anomaly_index = int(dpg.get_value("anomaly_to_remove")[-1])-1
    with open("modules/grav_anomaly/anomalies.json", "r+") as anomaly_file:
        parsed = json.load(anomaly_file)
        # Try to delete anomaly
        try:
            del parsed[anomaly_index]
            
            anomaly_file.seek(0)
            json.dump(parsed, anomaly_file, indent = 4)
            anomaly_file.truncate()
            anomaly_file.close()
            
            print(f"Anomaly {anomaly_index+1} was removed!")
        except:
            print(f"Anomaly{anomaly_index+1} was not found...")
    
    updateCurrentAnomalies()


def updateCurrentAnomalies():
    # Update anomalies in dropdown and in table
    print("Updating anomalies...")

    anomalies = getAnomalies()
    number_of_anomalies = len(anomalies)

    new_dropdown_values = [f"Anomaly {i+1}" for i in range(number_of_anomalies)]
    dpg.configure_item("anomaly_to_remove", items = new_dropdown_values)

    # Clear anomalies
    rows_to_clear = True
    i = 0
    while rows_to_clear:
        try:
            dpg.delete_item(f"row{i}")
            i += 1
        except:
            rows_to_clear = False

    # Now add the current anomalies
    for i in range(number_of_anomalies):
        values = [i+1, anomalies[i].x_pos,anomalies[i].dim,anomalies[i].drho,anomalies[i].depth]
        with dpg.table_row(parent="anomaly_table", tag=f"row{i}"):
            for j in range(len(values)):
                dpg.add_text(values[j])


def updatePlot():
    print("Generating plot...")

    x_min, x_max = dpg.get_value("x_min"), dpg.get_value("x_max")
    x_coords = np.linspace(x_min, x_max, 100)

    anomalies = getAnomalies()
    n_anomalies = len(anomalies)
    y_vals = np.zeros_like([x_coords]*n_anomalies)
    
    for i in range(n_anomalies):
        y_vals[i] = anomalies[i].computeAnomaly(x_coords=x_coords)
    
    # Try to update initial plot
    # If not already created then create new
    try:
        data_series_to_clear = True
        i = 0
        while data_series_to_clear:
            try:
                dpg.delete_item(f"Anomaly {i+1} series")
                i += 1
            except:
                data_series_to_clear = False
        dpg.delete_item("Sum series")
        for i in range(n_anomalies):
            dpg.add_line_series(x_coords, y_vals[i], label=f"Anomaly {i+1}", tag = f"Anomaly {i+1} series", parent="y_axis")
        
        # Add sum
        if n_anomalies > 1:
            dpg.add_line_series(x_coords, np.sum(y_vals,0), label="Sum", tag = "Sum series", parent="y_axis")
    except:
        with dpg.window(label = "Simulation", tag = "anomaly_plot_window", width=500, height=500,on_close=dpg.delete_item):
            dpg.add_text("To show legend - Right click chart and enable legend")
            with dpg.plot(label = "Gravity anomaly", width = -1, height = -25, tag = "anomaly_plot"):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="Gravity anomaly [mGal]", tag="y_axis")

                for i in range(n_anomalies):
                    dpg.add_line_series(x_coords, y_vals[i], label=f"Anomaly {i+1}", tag = f"Anomaly {i+1} series", parent="y_axis")
                
                # Add sum
                if n_anomalies > 1:
                    dpg.add_line_series(x_coords, np.sum(y_vals,0), label="Sum", tag = "Sum series", parent="y_axis")
            
            # Save data
            dpg.add_button(label = "Save figure/anomalies", callback=saveData)


def saveData():
    print("Saving data...")

    anomalies = getAnomalies()
    n_anomalies = len(anomalies)
    x_coords = dpg.get_value("Anomaly 1 series")[0]
    y_vals = np.zeros_like([x_coords]*n_anomalies)
    
    # Generate y values and add to plot
    for i in range(n_anomalies):
        y_vals[i] = anomalies[i].computeAnomaly(x_coords=x_coords)
        plt.plot(x_coords,y_vals[i], label= f"Anomaly {i+1}")
    
    plt.xlim((x_coords[0],x_coords[-1]))
    plt.title(f"Gravity anomaly")
    plt.xlabel(r"Distance [$m$]")
    plt.ylabel(r"Gravity anomaly [$mGal$]")
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"modules/grav_anomaly/Anomaly.jpg", dpi=150)
    
    # Add sum to plot, if there are more than one anomaly
    if n_anomalies > 1:
        plt.plot(x_coords,np.sum(y_vals,0), label = "Sum")
        plt.legend()
        plt.savefig(f"modules/grav_anomaly/Anomaly_sum.jpg", dpi=150)
    
    # TODO
    # Copy json file

    print("Finished saving...")
