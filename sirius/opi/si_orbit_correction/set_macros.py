from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil, ConsoleUtil

## PVS Database

# External PVs

# Beam Orbit
ref_orbit_x_pv = "SICO-SOFB-REFORBIT-X"
orbit_x_pv = "SICO-SOFB-AVGORBIT-X"
ref_orbit_x_sel_pv = "SICO-SOFB-REFORBIT-X-SEL"
ref_orbit_y_pv = "SICO-SOFB-REFORBIT-Y"
orbit_y_pv = "SICO-SOFB-AVGORBIT-Y"
ref_orbit_y_sel_pv = "SICO-SOFB-REFORBIT-Y-SEL"
bpm_pos_pv = "VA-SIFK-BPM-POS"

# Orbits
num_samples_pv = "SICO-SOFB-AVGORBIT-NUMSAMPLES"

# SOFB
sofb_weight_h_pv = "SICO-SOFB-WEIGHT-H"
sofb_weight_v_pv = "SICO-SOFB-WEIGHT-V"
sofb_mode_pv = "SICO-SOFB-MODE"
sofb_mode_plane_pv = "SICO-SOFB-MODE-PLANE"
sofb_mode_rffreq_pv = "SICO-SOFB-MODE-RFFREQ"
sofb_mancorr_pv = "SICO-SOFB-MANCORR"
sofb_error_pv = "SICO-SOFB-ERROR"

# Local PVs

# Beam Orbit
ref_orbit_x_locpv = "loc://ref_orbit_x(0)"
orbit_x_locpv = "loc://orbit_x(0)"
delta_orbit_x_locpv = "loc://delta_orbit_x(0)"
ref_orbit_y_locpv = "loc://ref_orbit_y(0)"
orbit_y_locpv = "loc://orbit_y(0)"
delta_orbit_y_locpv = "loc://delta_orbit_y(0)"
rms_x_locpv = "loc://rms_x(0)"
mean_x_locpv = "loc://mean_x(0)"
max_x_locpv = "loc://max_x(0)"
min_x_locpv = "loc://min_x(0)"
rms_y_locpv = "loc://rms_y(0)"
mean_y_locpv = "loc://mean_y(0)"
max_y_locpv = "loc://max_y(0)"
min_y_locpv = "loc://min_y(0)"

# Orbits
register_locpv = "loc://register(0)"
display_mode_locpv = "loc://display_mode(0)"
deviation_register_locpv = "loc://deviation_register(0)"
update_orbit_locpv = "loc://update_orbit(0)"

# SOFB
sofb_corr_h_locpv = "loc://sofb_corr_h(0)"
sofb_corr_v_locpv = "loc://sofb_corr_v(0)"
sofb_corr_coupling_locpv = "loc://sofb_coupling(0)"
sofb_corr_rffreq_locpv = "loc://sofb_corr_freq(0)"

# FOFB
fofb_corr_h_locpv = "loc://fofb_corr_h(0)"
fofb_corr_v_locpv = "loc://fofb_corr_v(0)"
fofb_corr_coupling_locpv = "loc://fofb_coupling(0)"


## Control Panel

# Get Widgets
control_panel = display.getWidget("Control Panel")

# Set Macros
control_panel_macros = DataUtil.createMacrosInput(True)
control_panel_macros.put("ref_orbit_x_ioc", ref_orbit_x_pv)
control_panel_macros.put("orbit_x_ioc", orbit_x_pv)
control_panel_macros.put("ref_orbit_x_ioc_sel", ref_orbit_x_sel_pv)
control_panel_macros.put("ref_orbit_y_ioc", ref_orbit_y_pv)
control_panel_macros.put("orbit_y_ioc", orbit_y_pv)
control_panel_macros.put("ref_orbit_y_ioc_sel", ref_orbit_y_sel_pv)
control_panel_macros.put("ref_orbit_x_graph", ref_orbit_x_locpv)
control_panel_macros.put("orbit_x_graph", orbit_x_locpv)
control_panel_macros.put("delta_orbit_x", delta_orbit_x_locpv)
control_panel_macros.put("ref_orbit_y_graph", ref_orbit_y_locpv)
control_panel_macros.put("orbit_y_graph", orbit_y_locpv)
control_panel_macros.put("delta_orbit_y", delta_orbit_y_locpv)
control_panel_macros.put("bpm_pos", bpm_pos_pv)
control_panel_macros.put("register", register_locpv)
control_panel_macros.put("display_mode", display_mode_locpv)
control_panel_macros.put("deviation_register", deviation_register_locpv)
control_panel_macros.put("update_orbit", update_orbit_locpv)
control_panel_macros.put("rms_x", rms_x_locpv)
control_panel_macros.put("mean_x", mean_x_locpv)
control_panel_macros.put("max_x", max_x_locpv)
control_panel_macros.put("min_x", min_x_locpv)
control_panel_macros.put("rms_y", rms_y_locpv)
control_panel_macros.put("mean_y", mean_y_locpv)
control_panel_macros.put("max_y", max_y_locpv)
control_panel_macros.put("min_y", min_y_locpv)
control_panel_macros.put("num_samples", num_samples_pv)
control_panel_macros.put("sofb_weight_h", sofb_weight_h_pv)
control_panel_macros.put("sofb_weight_v", sofb_weight_v_pv)
control_panel_macros.put("sofb_mode", sofb_mode_pv)
control_panel_macros.put("sofb_mode_plane", sofb_mode_plane_pv)
control_panel_macros.put("sofb_mode_rffreq", sofb_mode_rffreq_pv)
control_panel_macros.put("sofb_mancorr", sofb_mancorr_pv)
control_panel_macros.put("sofb_error", sofb_error_pv)
control_panel.setPropertyValue("macros", control_panel_macros)

# Reload OPI
control_panel.setPropertyValue("opi_file", "control_panel.opi")