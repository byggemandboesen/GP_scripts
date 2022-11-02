import dearpygui.dearpygui as dpg
import pandas as pd
import numpy as np

def bFieldRMSModule():
    with dpg.collapsing_header(label = "Magnetic field RMS"):
        dpg.add_text("Select degree and year of Gauss coefficients")

        df = loadFile()
        # Add options to select parameters
        n_degrees = [int(df["deg"].iloc[0]),int(df["deg"].iloc[-1])]
        years = [df.columns[i] for i in range(3,len(df.columns))]

        dpg.add_slider_int(label = "Degree", min_value=n_degrees[0], max_value=n_degrees[1], default_value = 1, tag = "b_rms_degree", callback = updateRMS)
        dpg.add_combo(years, label = "Year", default_value = years[-1], tag = "year", callback = updateRMS)
        # Year defults to most recent data

        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_text("Geomagnetic field RMS: ")
            dpg.add_text("NaN", tag = "rms_val")
            dpg.add_text("nT")
        updateRMS()


def updateRMS():
    '''
    Update RMS each time a new degree/year is selected
    '''
    df = loadFile()

    degree = dpg.get_value("b_rms_degree")
    year = dpg.get_value("year")

    rms = 0
    for i in range(0,degree+1):
        g = float(pd.to_numeric(df[str(year)][(df["deg"] == degree) & (df["ord"] == i) & (df["g/h"] == "g")]).to_numpy())
        h = float(pd.to_numeric(df[str(year)][(df["deg"] == degree) & (df["ord"] == i) & (df["g/h"] == "h")]).to_numpy()) if i > 0 else 0
        # print(f"g{i} = {g}")
        # print(f"h{i} = {h}")

        rms += (g**2+h**2)
    
    rms *= (degree + 1)
    
    dpg.set_value("rms_val", np.round(np.sqrt(rms),3))


# TODO Consider adding lookup function to find certain Gauss coefficients

def loadFile():
    df = pd.read_csv("modules/b_field_rms/Gauss_Coefficients.txt")
    return df

