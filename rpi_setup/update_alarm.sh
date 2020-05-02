#!/bin/bash

pialarm_dir="${HOME}/PieAlarm"

if [[ ! -d ${pialarm_dir} ]]; then
	git clone https://github.com/rmasp98/PieAlarm.git ${pialarm_dir}
else
	cd ${pialarm_dir}
	echo "Checking for updates"
	git pull 2>&1 > /dev/null

	if [[ $? == 1 ]]; then
		echo "There are some changes in the project. Do you want to pull a clean version? (Y/N)"
		read confirm
		if [[ "$confirm" == "Y" ]] || [[ "$confirm" == "y" ]]; then
			cd ${HOME}
			rm -rf ${pialarm_dir}
			git clone https://github.com/rmasp98/PieAlarm.git ${pialarm_dir} 2>&1 > /dev/null
		else
			echo "Exiting. Please fix problems before re-running script"
			exit
		fi
	fi
fi

echo "Install python dependencies"
pip3 install -r ${pialarm_dir}/requirements.txt

#echo "Copying Disney tracks to alarm"
#if [ ! -d sound/tracks/Disney ]; then
#	cp -r ~/Disney sound/tracks/
#fi

echo "Linking api key"
if [ ! -f api_key ]; then 
	ln -s ${HOME}/api_key ${pialarm_dir}/api_key
fi

if [[ "$1" == "start" ]]; then
	export DISPLAY=:0

	echo "Running alarm..."
	cd ${pialarm_dir}
	nohup python3 piealarm.py &
fi
