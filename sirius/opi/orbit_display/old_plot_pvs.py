from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil

length = len(pvs)-3
x = []
y = []

for i in range(length):
	if pvs[i].isConnected():
		x.append(i + 1)
		try:
			y.append(PVUtil.getDouble(pvs[i]))
		except:
			y.append(0)
			
xArray = DataUtil.toJavaDoubleArray(x)
yArray = DataUtil.toJavaDoubleArray(y)

pvArray[-3].setValue(xArray)
pvArray[-2].setValue(yArray)


