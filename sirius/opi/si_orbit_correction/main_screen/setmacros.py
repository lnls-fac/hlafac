from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil, ConsoleUtil

## PVS Database

# External PVs

# Beam Orbit
ref_orbit_x_pv = "SICO-SOFB-REFORBIT-X"
orbit_x_pv = "SICO-SOFB-AVGORBIT-X"
ref_orbit_y_pv = "SICO-SOFB-REFORBIT-Y"
orbit_y_pv = "SICO-SOFB-AVGORBIT-Y"
bpm_pos_pv = "VA-SIFK-BPM-POS"

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

# SOFB
sofb_weight_h_pv = "SICO-SOFB-WEIGHT-H"
sofb_weight_v_pv = "SICO-SOFB-WEIGHT-V"

# Local PVs

# Beam Orbit
ref_orbit_x_locpv = "loc://ref_orbit_x(0)"
orbit_x_locpv = "loc://orbit_x(0)"
delta_orbit_x_locpv = "loc://delta_orbit_x(0)"
ref_orbit_y_locpv = "loc://ref_orbit_y(0)"
orbit_y_locpv = "loc://orbit_y(0)"
delta_orbit_y_locpv = "loc://delta_orbit_y(0)"

# Orbits
register_locpv = "loc://register(0)"
display_mode_locpv = "loc://display_mode(0)"
deviation_register_locpv = "loc://deviation_register(0)"

# SOFB
sofb_corr_h_locpv = "loc://sofb_corr_h(0)"
sofb_corr_v_locpv = "loc://sofb_corr_v(0)"
sofb_corr_coupling_locpv = "loc://sofb_coupling(0)"
sofb_corr_freq_locpv = "loc://sofb_corr_freq(0)"


## Control Panel

# Get Widgets
control_panel = display.getWidget("Control Panel")

# Set Macros
control_panel_macros = DataUtil.createMacrosInput(True)
control_panel_macros.put("ref_orbit_x", ref_orbit_x_locpv)
control_panel_macros.put("orbit_x", orbit_x_locpv)
control_panel_macros.put("delta_orbit_x", delta_orbit_x_locpv)
control_panel_macros.put("ref_orbit_y", ref_orbit_y_locpv)
control_panel_macros.put("orbit_y", orbit_y_locpv)
control_panel_macros.put("delta_orbit_y", delta_orbit_y_locpv)
control_panel_macros.put("bpm_pos", bpm_pos_pv)
control_panel_macros.put("register", register_locpv)
control_panel_macros.put("display_mode", display_mode_locpv)
control_panel_macros.put("deviation_register", deviation_register_locpv)
control_panel_macros.put("rms_x", rms_x_pv)
control_panel_macros.put("mean_x", mean_x_pv)
control_panel_macros.put("max_x", max_x_pv)
control_panel_macros.put("min_x", min_x_pv)
control_panel_macros.put("rms_y", rms_y_pv)
control_panel_macros.put("mean_y", mean_y_pv)
control_panel_macros.put("max_y", max_y_pv)
control_panel_macros.put("min_y", min_y_pv)
control_panel_macros.put("num_samples", num_samples_pv)
control_panel_macros.put("sofb_weight_h", sofb_weight_h_pv)
control_panel_macros.put("sofb_weight_v", sofb_weight_v_pv)
control_panel_macros.put("sofb_corr_h", sofb_corr_h_locpv)
control_panel_macros.put("sofb_corr_v", sofb_corr_v_locpv)
control_panel_macros.put("sofb_corr_coupling", sofb_corr_coupling_locpv)
control_panel_macros.put("sofb_corr_freq", sofb_corr_freq_locpv)
control_panel.setPropertyValue("macros", control_panel_macros)

# Reload OPI
control_panel.setPropertyValue("opi_file", "")
control_panel.setPropertyValue("opi_file", "control_panel.opi")

