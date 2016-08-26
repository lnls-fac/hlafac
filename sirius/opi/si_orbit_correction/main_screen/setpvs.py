from org.csstudio.opibuilder.scriptUtil import PVUtil, WidgetUtil, DataUtil, ScriptUtil, GUIUtil, ConsoleUtil

## External PVs

# Beam Orbit
ref_orbit_x_pv = "SICO-SOFB-REFORBIT-X"
orbit_x_pv = "SICO-SOFB-AVGORBIT-X"
ref_orbit_y_pv = "SICO-SOFB-REFORBIT-Y"
orbit_y_pv = "SICO-SOFB-AVGORBIT-Y"

# Orbits
num_samples_pv = "SICO-SOFB-AVGORBIT-NUMSAMPLES"

# Statistical Data
rms_x_pv = "SICO-SOFB-ORBIT-X-RMS"
mean_x_pv = "SICO-SOFB-ORBIT-X-MEAN"
max_x_pv = "SICO-SOFB-ORBIT-X-MAX"
min_x_pv = "SICO-SOFB-ORBIT-X-MIN"
rms_y_pv = "SICO-SOFB-ORBIT-Y-RMS"
mean_y_pv = "SICO-SOFB-ORBIT-Y-MEAN"
max_y_pv = "SICO-SOFB-ORBIT-Y-MAX"
min_y_pv = "SICO-SOFB-ORBIT-Y-MIN"


## Control Panel

# Get Macros
ref_orbit_x_macro = display.getMacroValue("ref_orbit_x")
orbit_x_macro = display.getMacroValue("orbit_x")
delta_orbit_x_macro = display.getMacroValue("delta_orbit_x")
ref_orbit_y_macro = display.getMacroValue("ref_orbit_y")
orbit_y_macro = display.getMacroValue("orbit_y")
delta_orbit_y_macro = display.getMacroValue("delta_orbit_y")
bpm_pos_macro = display.getMacroValue("bpm_pos")
# register_macro = display.getMacroValue("register")
# display_mode_macro = display.getMacroValue("display_mode")
# deviation_register_macro = display.getMacroValue("deviation_register")

# Set Local PVs
register_locpv = "loc://register(1)"
display_mode_locpv = "loc://display_mode(1)"
deviation_register_locpv = "loc://deviation_register(1)"


## Beam Orbit

# Get Widgets
beam_orbit = display.getWidget("Beam Orbit")
graph_orbit_x = beam_orbit.getWidget("Graph Orbit X")
graph_orbit_y = beam_orbit.getWidget("Graph Orbit Y")

# Set PVs
graph_orbit_x.setPropertyValue("trace_0_x_pv", bpm_pos_macro)
graph_orbit_x.setPropertyValue("trace_0_y_pv", delta_orbit_x_macro)
graph_orbit_y.setPropertyValue("trace_0_x_pv", bpm_pos_macro)
graph_orbit_y.setPropertyValue("trace_0_y_pv", delta_orbit_y_macro)


## Orbits

# Get Widgets
orbits = display.getWidget("Orbits")
num_samples = orbits.getWidget("Num. Samples")
register_selection = orbits.getWidget("Register Selection")
registers = register_selection.getPropertyValue("items")
selected_register = orbits.getWidget("Selected Register")
display_mode = orbits.getWidget("Display Mode")
modes = display_mode.getPropertyValue("items")
deviation_register = orbits.getWidget("Deviation Register")

# Set PVs
num_samples.setPropertyValue("pv_name", num_samples_pv)
register_selection.setPropertyValue("pv_name", register_locpv)
selected_register.setPropertyValue("pv_name", register_locpv)
display_mode.setPropertyValue("pv_name", display_mode_locpv)
deviation_register.setPropertyValue("pv_name", deviation_register_locpv)

# Initial State
PVUtil.writePV(register_locpv, registers[0])
PVUtil.writePV(display_mode_locpv, modes[0])
PVUtil.writePV(deviation_register_locpv, registers[0])


## Statistical Data

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
