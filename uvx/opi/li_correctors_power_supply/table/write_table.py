from org.csstudio.opibuilder.scriptUtil import PVUtil, WidgetUtil, DataUtil

def get_power_supply_list():
    power_supplies = [
		"L-CV01A", "L-CH01A",
		"L-CV01B", "L-CH01B",
		"L-CV02", "L-CH02",
		]
    return power_supplies


def add_header(table, header_opi):
    linkingContainer = WidgetUtil.createWidgetModel("org.csstudio.opibuilder.widgets.linkingContainer")   
    linkingContainer.setPropertyValue("opi_file", header_opi)
    linkingContainer.setPropertyValue("resize_behaviour", 1)
    linkingContainer.setPropertyValue("border_style", 0)
    table.addChildToBottom(linkingContainer)


def add_line(table, line_opi, power_supply):
    linkingContainer = WidgetUtil.createWidgetModel("org.csstudio.opibuilder.widgets.linkingContainer")   
    linkingContainer.setPropertyValue("opi_file", line_opi)
    linkingContainer.setPropertyValue("resize_behaviour", 1)
    linkingContainer.setPropertyValue("border_style", 0)
    table.addChildToBottom(linkingContainer)

    setpoint = subsystem + power_supply.upper() + ':SlowReferenceCurrent'
    readback = subsystem + power_supply.upper() + ':OutputCurrent'
    on_off = subsystem + power_supply.upper() + ':OnOff'
    command_mode = subsystem + power_supply.upper() + ':CommandMode'
    command = subsystem + power_supply.upper() + ':Command'
    interlock = subsystem + power_supply.upper() + ':HardInterlocks'
    
    macro_inputs = DataUtil.createMacrosInput(True)
    macro_inputs.put("power_supply", power_supply)
    macro_inputs.put("power_supply_sp", setpoint)
    macro_inputs.put("power_supply_rb", readback)
    macro_inputs.put("power_supply_on_off", on_off)
    macro_inputs.put("power_supply_command_mode", command_mode)
    macro_inputs.put("power_supply_command", command)
    macro_inputs.put("power_supply_interlock", interlock)
    linkingContainer.setPropertyValue("macros", macro_inputs)
    
    children = linkingContainer.getChildren()
    for w in children:
        if w.getPropertyValue("widget_type") == "Action Button":
            button = w
        elif w.getPropertyValue("widget_type") == "Spinner":
            spinner = w
        elif w.getPropertyValue("widget_type") == "Text Update":
            text_update = w
        elif w.getPropertyValue("name") == "Grouping Container_OnOff":
            container = w
            led_on_off = container.getChildren()[0]  
        elif w.getPropertyValue("name") == "Grouping Container_Failure":
            container = w
            led_interlock = container.getChildren()[0]          
 
    button.setPropertyValue("text", power_supply)
    spinner.setPropertyValue("pv_name", setpoint)
    text_update.setPropertyValue("pv_name", readback)
    led_on_off.setPropertyValue("pv_name", on_off)
    led_interlock.setPropertyValue("pv_name", interlock)

    
subsystem      = "UVX:LINAC:"
header_opi     = "table/table_header.opi"
line_opi       = "table/table_line.opi"
power_supplies = get_power_supply_list()
table          = display.getWidget("Table")
    
if power_supplies is None:
    table.setPropertyValue("visible", False)
else:
    add_header(table, header_opi)    
    for ps in power_supplies:
        add_line(table, line_opi, ps)   
    table.performAutosize()            
    table.setPropertyValue("visible", True)
