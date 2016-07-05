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
    
    children = linkingContainer.getChildren()
    for w in children:
        if w.getPropertyValue("widget_type") == "Action Button":
            button = w
        elif w.getPropertyValue("widget_type") == "Spinner":
            spinner = w
        elif w.getPropertyValue("widget_type") == "Text Update":
            text_update = w
        elif w.getPropertyValue("widget_type") == "Grouping Container":
            container = w
            led = container.getChildren()[0]  
        
    setpoint = subsystem + power_supply.upper() + ':SlowReferenceCurrent'
    readback = subsystem + power_supply.upper() + ':OutputCurrent'
    status = subsystem + power_supply.upper() + ':OnOff'
    control = subsystem + power_supply.upper() + ':CommandMode'
    interlock = subsystem + power_supply.upper() + ':HardInterlocks'
    command = subsystem + power_supply.upper() + ':Command'

    macro_inputs = DataUtil.createMacrosInput(True)
    macro_inputs.put("power_supply", power_supply)
    macro_inputs.put("power_supply_sp", setpoint)
    macro_inputs.put("power_supply_rb", readback)
    macro_inputs.put("power_supply_status", status)
    macro_inputs.put("power_supply_control", control)
    macro_inputs.put("power_supply_interlock", interlock)
    macro_inputs.put("power_supply_command", command)
    linkingContainer.setPropertyValue("macros", macro_inputs)
  
    button.setPropertyValue("text", power_supply)
    spinner.setPropertyValue("pv_name", setpoint)
    text_update.setPropertyValue("pv_name", readback)
    led.setPropertyValue("pv_name", status)

    
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
