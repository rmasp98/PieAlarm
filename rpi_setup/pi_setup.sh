#!/bin/bash

# Script to setup raspbian for PieAlarm

background_url="https://github.com/rmasp98/PieAlarm/raw/master/ui/icons/landscape.jpg"
alarm_update_url="https://raw.githubusercontent.com/rmasp98/PieAlarm/master/rpi_setup/alarm_util.sh"


###########################################################
if [[ "${EUID}" != 0 ]]; then
	echo "Please run as sudo or root"
	exit
fi

############################################################
echo "Updating and installing all required packages"
apt update && apt dist-upgrade -y
apt install -y  portaudio19-dev ffmpeg python3 python3-pip python3-pyqt5 xserver-xorg xinit git vim-gtk3 mingetty feh 
if [[ $? != 0 ]]; then echo "Package install failed!"; exit; fi

############################################################
echo "Enter new hostname:" && read hostname
echo "${hostname}" > /etc/hostname

#############################################################
profile="/etc/profile"
if ! grep -q "exec startx" ${profile}; then
	echo "Adding startx details to ${profile}"
	cat >> ${profile} <<'EOF'
if [[ "$(tty)" == '/dev/tty8' ]]; then
	exec startx
fi
EOF
fi

##############################################################
echo "Creating new user. Username:" && read username
home_dir="/home/${username}"
if ! id -u ${username} > /dev/null 2>&1; then
	useradd -m -G sudo ${username}
	passwd ${username}
else
	echo "User already exists"
fi

###############################################################
x11_service="/etc/systemd/system/x11.service"
echo "Creating autologin service in ${x11_service}"
cat > ${x11_service} <<EOF
[Unit]
After=systemd-user-sessions.service

[Service]
ExecStart=/sbin/mingetty --autologin ${username} --noclear tty8 38400

[Install]
WantedBy=multi-user.target
EOF
systemctl enable x11.service

#################################################################
pialarm_dir="${home_dir}/PieAlarm"
echo "Setting up the PieAlarm"
echo "Please provide the darksky api key:" && read darksky_key
if [[ "${darksky_key}" == "" ]]; then
	echo "An empty API key will cause weather to fail in the PieAlarm app"
fi
echo ${darksky_key} > ${home_dir}/api_key


echo "Pulling down script to set up PieAlarm"
update_script="${home_dir}/update_alarm.sh"
wget ${update_script_url} -O ${update_script}
if [[ $? != 0 ]]; then echo "There was an error retrieving the update_alarm.sh script"; exit; fi
chmod u+x ${update_script}
${update_script} update -d ${home_dir}/PieAlarm
if [[ $? != 0 ]]; then echo "There was an error in the update_alarm.sh script"; exit; fi

##################################################################
xsession_file="${home_dir}/.xsession"
echo "Creating .xsession file for ${username} in ${xsession_file}"
cat > ${xsession_file} <<EOF 
${update_script} start &
feh --bg-fill ${home_dir}/.config/background.jpg
exec sleep infinity
EOF

blank_file="/etc/X11/xorg.conf.d/10-monitor.conf"
echo "Preventing xorg from screen blanking in ${blank_file}"
mkdir -p /etc/X11/xorg.conf.d/
cat > ${blank_file} <<EOF
Section "Monitor"
    Identifier "LVDS0"
    Option "DPMS" "false"
EndSection

Section "ServerLayout"
    Identifier "ServerLayout0"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime"     "0"
    Option "BlankTime"   "0"
EndSection
EOF

echo "Pulling down background image"
mkdir ${home_dir}/.config
wget ${background_url} -O ${home_dir}/.config/background.jpg

#########################################################################
echo "Setting up SSH. Please provide alert URL:" && read alert_url
alert_file="/root/.local/bin/alert.sh"
mkdir -p /root/.local/bin
echo "Writing alert script to ${alert_file}"
cat > ${alert_file} <<EOF
#!/bin/bash

if [ "\${PAM_TYPE}" = "open_session" ]; then
        # This will send a message to the slack channel warning me that someone has logged on
        curl -X POST -H 'Content-type: application/json' \
                --data "{\"text\":\"<!channel> [ALERT] Someone has logged onto \${HOSTNAME} as \${PAM_USER}\"}" \
                ${alert_url} \
                2&> /dev/null;
fi
exit 0
EOF
chmod u+x ${alert_file}

sshd_file="/etc/ssh/sshd_config"
echo "Creating the sshd config file in ${sshd_file}"
mv ${sshd_file} ${sshd_file}.old
cat > ${sshd_file} <<EOF
PermitRootLogin no
PasswordAuthentication no
PermitEmptyPasswords no
PubkeyAuthentication yes
IgnoreRhosts yes
HostbasedAuthentication no
AllowUsers ${username}
DenyUsers root
ClientAliveInterval 1800
ClientAliveCountMax 0
Banner /etc/issue
UsePAM yes
AuthenticationMethods publickey
ChallengeResponseAuthentication no
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
EOF

pam_file="/etc/pam.d/sshd"
if ! grep -q "/root/.local/bin/alert.sh" ${pam_file}; then
	echo "Adding alert.sh to ${pam_file}"
	echo "session	   required     pam_exec.so   /root/.local/bin/alert.sh" >> ${pam_file}
fi

echo "Paste in you public SSH key. Make sure it is correct as you will be locked out of the raspberry pi if it is not. Leave blank if you want to retain password based SSH" && read ssh_key
if [[ "${ssh_key}" != "" ]]; then
	echo "Adding SSH key to ${home_dir}/.ssh/authorized_keys"
	mkdir -p ${home_dir}/.ssh
	echo ${ssh_key} > ${home_dir}/.ssh/authorized_keys
else
	echo "Changing AuthenticationMethod to password for SSH"
	sed -i 's/AuthenticationMethods publickey/AuthenticationMethods password/g' ${sshd_file}
	sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' ${sshd_file}
fi


###################################################################################
brightness_file="/sys/class/backlight/rpi_backlight/brightness"
cron_file="/etc/crontab"
echo "Adding temporary brightness cron jobs to ${cron_file} until light sensor implemented"
cat >> ${cron_file} <<EOF
30 6    * * *   root    echo 100 > ${brightness_file}
30 9    * * *   root    echo 16 > ${brightness_file}
30 22   * * *   root    echo 9 > ${brightness_file}
EOF

##################################################################################
udev_file="/etc/udev/rules.d/70-mote.rules"
echo "Writing permissions for ${username} to control mote LEDs in ${udev_file}"
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"16d0\", ATTRS{idProduct}==\"08c4\", OWNER=\"${username}\"" > ${udev_file}

#################################################################################
sound_file="/etc/asound.conf"
echo "Setting pi hat as the default sounds card"
cat > ${sound_file} <<EOF
defaults.ctl.card 1;
defaults.pcm.card 1;
EOF

echo "Setting default master volume to 40%"
amixer set Master 40%
alsactl store

##################################################################################
echo "Giving ownership of all created files in ${home_dir} to ${username}"
chown ${username}:${username} -R ${home_dir}

echo "Removing pi user"
userdel -rf pi
