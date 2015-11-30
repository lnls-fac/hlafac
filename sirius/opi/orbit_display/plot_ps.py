from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil
import java.util.ArrayList
import math

ps_pos_pv   = pvArray[-3]
ps_pv     = pvArray[-2]

try:
    ps_pos = PVUtil.getDoubleArray(ps_pos_pv)
    length  = len(ps_pos)
    
    # Plot diference from reference orbit
    ps = []
    for i in range(length):
        try:
            ps.append(PVUtil.getDouble(pvs[i]))
        except:
            ps.append(0.0)
    ps_pv.setValue(DataUtil.toJavaDoubleArray(ps))
    
    # Set y axis limits
    y = [math.fabs(j) for j in ps]
    default = 10
    maximum = max(y) if len(y) > 0 else default
    if maximum <= default:
        widget.setPropertyValue("axis_1_maximum",  default)
        widget.setPropertyValue("axis_1_minimum", -default)
    else:
        widget.setPropertyValue("axis_1_maximum",  maximum)
        widget.setPropertyValue("axis_1_minimum", -maximum)
except:
    pass