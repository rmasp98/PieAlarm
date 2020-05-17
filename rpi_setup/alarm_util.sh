#!/bin/bash

git_repo="https://github.com/rmasp98/PieAlarm.git"

function update {
    pialarm_dir=$1
    quiet=$2

    if [[ ! -d ${pialarm_dir} ]]; then
	    git clone ${git_repo} ${pialarm_dir}
    else
	    cd ${pialarm_dir}
	    echo "Checking for updates"
	    git pull 2>&1 > /dev/null

	    if [[ $? != 0 ]]; then
		    echo "There are some changes in the project. Do you want to pull a clean version? (Y/N)"
		    read confirm
		    if [[ "$confirm" == "Y" ]] || [[ "$confirm" == "y" ]]; then
			    cd ${HOME}
			    rm -rf ${pialarm_dir}
			    git clone ${git_repo} ${pialarm_dir} 2>&1 > /dev/null
		    else
			    echo "Exiting. Please fix problems before re-running script"
			    return
		    fi
	    fi
    fi
    
    if [[ ! ${quiet} ]]; then
        echo "Install python dependencies"
        sudo pip3 install -r ${pialarm_dir}/requirements.txt
    fi
}

function run {
    pialarm_dir=$1

    echo "Linking api key"
    if [ ! -f api_key ]; then 
	    ln -s ${HOME}/api_key ${pialarm_dir}/api_key
    fi

    export DISPLAY=:0

	echo "Running alarm..."
	cd ${pialarm_dir}
	nohup python3 piealarm.py &
}

function help_main {
	echo "Usage: cmd subcmd [options]"
        echo "  subcommands:"
        echo "      update      download or update git repository"
        echo "      run         run piealarm"
}

function help_update {
	echo "Usage: cmd update [-d dir] [-q] [-h]"
	echo "  Options:"
	echo "    -d dir  directory that the repo will/is installed to"
	echo "    -q      prevent pip install which requires sudo"
	echo "    -h      shows this page"
}

function help_run {
	echo "Usage: cmd run [-d dir] [-q] [-u] [-h]"
	echo "  Options:"
	echo "    -d dir  directory that the repo will/is installed to"
	echo "    -q      prevent pip install which requires sudo"
	echo "    -u      update as well as run"
	echo "    -h      shows this page"
}



while getopts "h" opt; do
    case ${opt} in
        h)
		help_main
                exit 0
        	;;
	\?)
		help_main
		exit 1
		;;
    esac
done
shift $((OPTIND -1))

quiet=false
subcommand=$1; shift
case "${subcommand}" in
	update)
        	while getopts ":d:qh" opt; do
            		case ${opt} in
                		d)
                    			dir=${OPTARG}
                    			;;
                		q)
                    			quiet=true
                    			;;
                		h)
                    			help_update
					exit 0
					;;
				\?)
					help_update
					exit 1
					;;
            		esac
        	done
		if [[ "${dir}" != "" ]]; then
        		update ${dir} ${quiet}
		else
			echo "Please specify the directory"
			help_update
			exit 1
		fi
		;;
	run)
        	update=false
        	while getopts ":d:quh" opt; do
            		case ${opt} in
                		d)
                    			dir=${OPTARG}
                    			;;
                		q)
                    			quiet=true
                    			;;
                		u)
                    			update=true
                    			;;
                		h)
                    			help_run
					exit 0
                    			;;
				\?)
					help_run
					exit 1
					;;
            		esac
        	done
		if [[ "${dir}" != "" ]]; then
	        	if [[ ${update} ]]; then
        	    		update ${dir} ${quiet}
        		fi
        		run ${dir}
		else
			echo "Please specify directory"
			help_run
			exit 1
		fi
        	;;
	*)
		help_main
		exit 0
		;;
esac
