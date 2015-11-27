from org.csstudio.opibuilder.scriptUtil import PVUtil, DataUtil

length = len(pvs)-3
orbit = []

try:
	ref_orbit = PVUtil.getDoubleArray(pvArray[-3])
except:
	ref_orbit = [0]*length

for i in range(length):
	try:
		orbit.append(PVUtil.getDouble(pvs[i]) - ref_orbit[i])
	except:
		orbit.append(0)
			
yArray = DataUtil.toJavaDoubleArray(orbit)
pvArray[-2].setValue(yArray)




