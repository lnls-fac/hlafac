from org.csstudio.opibuilder.scriptUtil import PVUtil
import java.util.ArrayList

x = PVUtil.getDoubleArray(pvArray[0])
length = len(x)

ax        = widget.axisList[0]
ticklabel = ax.getScaleTickLabels()
labels    = []
positions = []
index = [j for j in range(5,length+1,5)]
index = [1] + index
for i in index:
    labels.append(str(i))
    positions.append(ax.getValuePosition(x[i-1],1))

ticklabel.tickLabels            = java.util.ArrayList(labels)
ticklabel.tickLabelPositions    = java.util.ArrayList(positions)
ticklabel.tickLabelVisibilities = java.util.ArrayList([True]*len(labels))
ax.setShowMajorGrid(1)
