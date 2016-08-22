from org.csstudio.opibuilder.scriptUtil import PVUtil, WidgetUtil, DataUtil, ScriptUtil, GUIUtil, ConsoleUtil

## PV database

#Beam Orbit
bpm_pos_pv = "VA-SIFK-BPM-POS"
reforbit_x_pv = "SICO-SOFB-REFORBIT-X"
orbit_x_pv = "SICO-SOFB-AVGORBIT-X"
reforbit_y_pv = "SICO-SOFB-REFORBIT-Y"
orbit_y_pv = "SICO-SOFB-AVGORBIT-Y"

# Orbits
num_samples_pv = "SICO-SOFB-AVGORBIT-NUMSAMPLES"

# Statistical Data
rms_x_pv = "SICO-SOFB-ORBIT-X-RMS"
mean_x_pv = "SICO-SOFB-ORBIT-X-RMS"
max_x_pv = "SICO-SOFB-ORBIT-X-MAX"
min_x_pv = "SICO-SOFB-ORBIT-X-MIN"
rms_y_pv = "SICO-SOFB-ORBIT-Y-RMS"
mean_y_pv = "SICO-SOFB-ORBIT-Y-MEAN"
max_y_pv = "SICO-SOFB-ORBIT-Y-MAX"
min_y_pv = "SICO-SOFB-ORBIT-Y-MIN"


## Beam Orbit

# Get Widgets
beam_orbit = display.getWidget("Beam Orbit")
graph_orbit_x = beam_orbit.getWidget("Graph Orbit X")
graph_orbit_y = beam_orbit.getWidget("Graph Orbit Y")

# Set PVs
display_orbit_x_pv = PVUtil.createPV("loc://orbit_x", beam_orbit)
graph_orbit_x.setPropertyValue("trace_0_x_pv", bpm_pos_pv)
graph_orbit_x.setPropertyValue("trace_0_y_pv", display_orbit_x_pv)
display_orbit_y_pv = PVUtil.createPV("loc://orbit_y", beam_orbit)
graph_orbit_y.setPropertyValue("trace_0_x_pv", bpm_pos_pv)
graph_orbit_y.setPropertyValue("trace_0_y_pv", display_orbit_y_pv)



## Orbits Widget

# Get Widgets
orbits = display.getWidget("Orbits")
num_samples = orbits.getWidget("Num. Samples")

# Set PVs
num_samples.setPropertyValue("pv_name", num_samples_pv)


## Statistical Data Widget

# Get Widgets
stat_data = display.getWidget("Statistical Data")
stat_data_x = stat_data.getWidget("X Plane")
rms_x = stat_data_x.getWidget("RMS")
mean_x = stat_data_x.getWidget("Mean")
max_x = stat_data_x.getWidget("Max")
min_x = stat_data_x.getWidget("Min")
stat_data_y = stat_data.getWidget("Y Plane")
rms_y = stat_data_y.getWidget("RMS")
mean_y = stat_data_y.getWidget("Mean")
max_y = stat_data_y.getWidget("Max")
min_y = stat_data_y.getWidget("Min")

# Set PVs
rms_x.setPropertyValue("pv_name", rms_x_pv)
mean_x.setPropertyValue("pv_name", mean_x_pv)
max_x.setPropertyValue("pv_name", max_x_pv)
min_x.setPropertyValue("pv_name", min_x_pv)
rms_y.setPropertyValue("pv_name", rms_y_pv)
mean_y.setPropertyValue("pv_name", mean_y_pv)
max_y.setPropertyValue("pv_name", max_y_pv)
min_y.setPropertyValue("pv_name", min_y_pv)

