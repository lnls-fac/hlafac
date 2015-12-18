# Destination directory
DEST_DIR = /opt/css/sns-css-4.1.0/dropins

GENERALSCRIPTS = \
		org.csstudio.csdata_3.2.0.201506301858.jar\
		org.csstudio.opibuilder_4.0.103.201506301920.jar\
		org.csstudio.opibuilder.customizedSpinner_2.0.0.201512180800.jar\
		org.csstudio.opibuilder.widgetExample_2.0.0.201512161402.jar\
		org.csstudio.simplepv_1.0.0.201506301920.jar\
		org.csstudio.ui.util_4.0.0.201506301858.jar\
		org.eclipse.core.runtime_3.10.0.v20140318-2214.jar\
		org.eclipse.draw2d_3.9.101.201408150207.jar\
		org.eclipse.gef_3.9.100.201408150207.jar\
		org.eclipse.osgi.util_3.3.0.v20131023-1243.jar\
		org.eclipse.ui_3.106.1.v20141002-1150.jar\
		org.eclipse.ui.views_3.7.0.v20140408-0703.jar\
		org.epics.vtype_2.9.1.20150630110613.jar


SCRIPTS = $(GENERALSCRIPTS)

FULLSCRIPTS = $(addprefix $(DEST_DIR)/, $(SCRIPTS))

install: uninstall $(SCRIPTS)
	cp $(SCRIPTS) $(DEST_DIR)

uninstall:
	-rm -rf $(FULLSCRIPTS)

develop: uninstall $(SCRIPTS)
	ln -srf $(SCRIPTS) $(DEST_DIR)
