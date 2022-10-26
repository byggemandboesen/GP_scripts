import sys
import dearpygui.dearpygui as dpg

# Import modules
# sys.path.append("modules/")
from modules.grav_anomaly import grav_anomaly
from modules.b_field_rms import b_field_rms

# Run user intereface
def run_ui():
    dpg.create_context()
    dpg.create_viewport(title='Geo and planetary physics 1 - Victor Boesen', width=1000, height=750)
    
    with dpg.window(label = "Modules", width = 500, height = 400, pos=[10,10], no_close=True):
        grav_anomaly.gravityAnomalyModule()
        b_field_rms.bFieldRMSModule()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    run_ui()