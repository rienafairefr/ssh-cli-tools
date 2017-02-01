Installing ssh-cli-tools
========================

You may install on:
- your dev PC, or
- an iotlab ssh frontend


Installing on an iotlab ssh frontend
------------------------------------

we recommend using a virtualenv

	virtualenv xx
	. xx/bin/activate
	git clone git@github.com:iot-lab/ssh-cli-tools.git
	cd ssh-cli-tools/
	pip install pip --upgrade
	pip install .
	open-a8-cli


Installing on your dev PC
-------------------------

we recommend using a virtual environment

you will need pip (version 9.0.1+ known to work)

	sudo apt-get-install virtualenvwrapper
	sudo apt-get install pip

	mkvirtualenv xx
	git clone git@github.com:iot-lab/ssh-cli-tools.git
	cd ssh-cli-tools/
	pip install .
	open-a8-cli
