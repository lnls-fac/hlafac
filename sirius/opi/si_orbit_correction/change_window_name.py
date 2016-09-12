from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.eclipse.ui import PlatformUI

## Define Window Title
title = PVUtil.getString(pvArray[1])

## Set Window Title
window = PlatformUI.getWorkbench().getActiveWorkbenchWindow()
window.getShell().setText(title)

