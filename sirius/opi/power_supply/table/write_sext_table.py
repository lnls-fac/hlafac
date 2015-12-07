from org.csstudio.opibuilder.scriptUtil import PVUtil, WidgetUtil

def get_power_supply_list():
    power_supplies = [
        'SFA-FAM',  'SDA-FAM',  'SD1J-FAM', 'SF1J-FAM',
        'SD2J-FAM', 'SD3J-FAM', 'SF2J-FAM', 'SF2K-FAM',
        'SD3K-FAM', 'SD2K-FAM', 'SF1K-FAM', 'SD1K-FAM',
        'SDB-FAM',  'SFB-FAM',  
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
        
    ps_name = power_supply.replace("-", "_").lower()
    button_name = "b_" + ps_name
    button.setPropertyValue("name", button_name)
    button.setPropertyValue("text", power_supply.replace("-FAM", ""))
    
    setpoint = subsystem + power_supply.upper() + '-SP'
    spinner_name = "sp_" + ps_name
    spinner.setPropertyValue("name", spinner_name)
    spinner.setPropertyValue("pv_name", setpoint)

    readback = subsystem + power_supply.upper() + '-RB' 
    text_update_name = "rb_" + ps_name
    text_update.setPropertyValue("name", text_update_name)
    text_update.setPropertyValue("pv_name", readback)
    text_update.setPropertyValue("horizontal_alignment", 1)

    led_name = "st_" + ps_name
    led.setPropertyValue("name", led_name)
    

subsystem      = "SIPS-"
header_opi     = "table/big_table_header.opi"
line_opi       = "table/big_table_line.opi"

power_supplies   = get_power_supply_list()
len_ps           = len(power_supplies)
nr_tables        = 1
table_container  = display.getWidget("table_container")
tables = []
for i in range(nr_tables):
    table = display.getWidget("table_%i"%(i+1))
    table.removeAllChildren()
    tables.append(table)
    
if power_supplies is None:
    table_container.setPropertyValue("visible", False)
    
else:
    j = 0
    for table in tables:
        add_header(table, header_opi)    
        for i in range(1,len_ps+1):
            power_supply = power_supplies[j]
            add_line(table, line_opi, power_supply)   
            j += 1
        table.performAutosize()
                
    table_container.setPropertyValue("visible", True)