from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil
import java.util.ArrayList
import math

ref_orbit_pv = pvArray[-4]
bpm_pos_pv   = pvArray[-3]
orbit_pv     = pvArray[-2]

try:
    bpm_pos = PVUtil.getDoubleArray(bpm_pos_pv)
    length  = len(bpm_pos)
   
    # Plot diference from reference orbit
    ref_orbit = PVUtil.getDoubleArray(ref_orbit_pv)
    orbit = []
    for i in range(length):
        try:
            orbit.append(PVUtil.getDouble(pvs[i]) - ref_orbit[i])
        except:
            orbit.append(0.0)           
    orbit_pv.setValue(DataUtil.toJavaDoubleArray(orbit))

    # Set y axis limits
    y = [math.fabs(j) for j in orbit]
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