from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil, ConsoleUtil
from math import sqrt

rms_pv = pvArray[1]
mean_pv = pvArray[2]
max_pv = pvArray[3]
min_pv = pvArray[4]

try:
        y = PVUtil.getDoubleArray(pvArray[0])
		
        rms_val = sqrt(sum([pow(y_i,2) for y_i in y])/len(y))
        mean_val = sum(y)/len(y)
        max_val = max(y)
        min_val = min(y)

        widget.getWidget("RMS").setPropertyValue("text", round(rms_val,4))
        widget.getWidget("Mean").setPropertyValue("text", round(mean_val,4))
        widget.getWidget("Max").setPropertyValue("text", round(max_val,4))
        widget.getWidget("Min").setPropertyValue("text", round(min_val,4))
except:
        pass
