PACKAGE=siriushlafac
PREFIX=
PIP=pip
ifeq ($(CONDA_PREFIX),)
	PREFIX=sudo -H
	PIP=pip-sirius
endif

install: clean uninstall
	$(PREFIX) $(PIP) install --no-deps --compile ./

uninstall:
	$(PREFIX) $(PIP) uninstall -y $(PACKAGE)

develop-install: clean develop-uninstall
	$(PIP) install --no-deps -e ./

# known issue: It will fail to uninstall scripts
#  if they were installed in develop mode
develop-uninstall:
	$(PIP) uninstall -y $(PACKAGE)

clean:
	git clean -fdX
