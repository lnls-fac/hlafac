DISTPATH=$(shell python-sirius -c "import site; print(site.getsitepackages())" | cut -f2 -d"'")
PACKAGE=siriushlafac
ISINST=$(shell sudo pip-sirius show $(PACKAGE) | wc -l )
EGGLINK=$(DISTPATH)/$(PACKAGE).egg-link
TMPFOLDER=/tmp/install-$(PACKAGE)


install: clean uninstall
	sudo ./setup.py install --single-version-externally-managed --compile --force --record /dev/null

develop: clean uninstall
	sudo -H pip-sirius install --no-deps -e ./

uninstall:
ifneq (,$(wildcard $(EGGLINK)))
	sudo rm -r $(EGGLINK)
endif
ifneq ($(ISINST),0)
	sudo -H pip-sirius uninstall -y $(PACKAGE)
	sed -i '/$(PACKAGE)/d' $(DISTPATH)/easy-install.pth
else
	echo 'already uninstalled $(PACKAGE)'
endif

clean:
	git clean -fdX
