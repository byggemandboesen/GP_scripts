import json
import numpy as np
import dearpygui.dearpygui as dpg

from modules.grav_anomaly.anomaly import Anomaly

def gravityAnomalyWindow():
    with dpg.collapsing_header(label = "Gravity anomalies"):
        dpg.add_text("Add, remove or simulate anomalies")
        print("Listing anomalies")


        
        with dpg.tree_node(label = "Anomalies"):
            anomalies = getAnomalies()


        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_input_float(label = "x-min", tag = "x_min", width = 100)
            dpg.add_input_float(label = "x-max", tag = "x_max", width = 100)

        dpg.add_button(label = "Simulate",callback=updatePlot)

# TODO
# Create add/remove system
# Create plot function

def getAnomalies():
    '''
    Returns a list of anomaly objects
    '''
    print("Getting anomalies")
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
    print(anomalies)
    return anomalies

def addAnomaly(info):
    print("Adding anomaly")

def updatePlot():
    x_coords = np.linspace(dpg.get_value("x_min"), dpg.get_value("x_max"))
    print("Updating plot")

