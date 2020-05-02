#!/bin/bash

# Script to setup raspbian for PieAlarm

############################################################
echo "Updating and installing all required packages"
apt update && apt dist-upgrade -y
apt install -y  portaudio19-dev python3 python3-pip python3-pyqt5 xserver-xorg xinit git vim-gtk3 mingetty feh 

############################################################
echo "Enter new hostname:" && read hostname
echo "${hostname}" > /etc/hostname

#############################################################
profile="/etc/profile"
echo "Adding startx details to ${profile}"
cat >> ${profile} <<'EOF'
if [[ "$(tty)" == '/dev/tty8' ]]; then
	exec startx
fi
EOF

##############################################################
echo "Creating new user. Username:" && read username
useradd -m -G sudo ${username}
passwd ${username}

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
pialarm_dir="/home/${username}/PieAlarm"
echo "Setting up the PieAlarm"
echo "Please provide the darksky api key:" && read darksky_key
echo ${darksky_key} > /home/${username}/api_key

echo "Pulling down script to set up PieAlarm"
update_script="/home/${username}/update_alarm.sh"
wget https://raw.githubusercontent.com/rmasp98/PieAlarm/master/rpi_setup/update_alarm.sh -O ${update_script}
${update_script}

##################################################################
xsession_file="/home/${username}/.xsession"
echo "Creating .xsession file for ${username} in ${xsession_file}"
cat > ${xsession_file} <<EOF 
${update_script} start &
feh --bg-fill /home/${username}/.config/background.jpg
exec sleep infinity
EOF
chown ${username}:${username} ${xsession_file}

echo "Preventing xorg from screen blanking in "
mkdir -p /etc/X11/xorg.conf.d/
cat > /etc/X11/xorg.conf.d/10-monitor.conf <<EOF
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
mkdir /home/${username}/.config
wget https://github.com/rmasp98/PieAlarm/raw/master/ui/icons/landscape.jpg -O /home/${username}/.config/background.jpg

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
echo "Adding alert.sh to ${pam_file}"
echo "session	   required     pam_exec.so   /root/.local/bin/alert.sh" >> ${pam_file}


###################################################################################
brightness_file="/sys/class/backlight/rpi_backlight/brightness"
cron_file="/var/spool/cron/crontabs/root"
echo "Adding temporary brightness cron jobs to ${cron_file} until light sensor implemented"
cat >> ${cron_file} <<EOF
30 6 * * * echo 100 > ${brightness_file}
30 9 * * * echo 16 > ${brightness_file}
30 10 * * * echo 9 > ${brightness_file}
EOF
