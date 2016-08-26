from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil, ConsoleUtil

## External PVs
bpm_pos_pv = "VA-SIFK-BPM-POS"


## Control Panel

# Get Widgets
control_panel = display.getWidget("Control Panel")

# Set Macros
control_panel_macros = DataUtil.createMacrosInput(True)
control_panel_macros.put("ref_orbit_x", "loc://ref_orbit_x")
control_panel_macros.put("orbit_x", "loc://orbit_x")
control_panel_macros.put("delta_orbit_x", "loc://delta_orbit_x")
control_panel_macros.put("ref_orbit_y", "loc://ref_orbit_y")
control_panel_macros.put("orbit_y", "loc://orbit_y")
control_panel_macros.put("delta_orbit_y", "loc://delta_orbit_y")
control_panel_macros.put("bpm_pos", bpm_pos_pv)
# control_panel_macros.put("register", "loc://register")
# control_panel_macros.put("display_mode", "loc://display_mode")
# control_panel_macros.put("deviation_register", "loc://deviation_register")
control_panel.setPropertyValue("macros", control_panel_macros)

# Reload OPI
control_panel.setPropertyValue("opi_file", "")
control_panel.setPropertyValue("opi_file", "control_panel.opi")
