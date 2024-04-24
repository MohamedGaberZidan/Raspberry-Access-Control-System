cd /etc/xdg/lxsession/LXDE-pi
sudo cp autostart autostartback
sudo bash -c 'echo "@lxterminal -e python3 /home/zidan/Raspberry-Access-Control-System/qr.py">>autostart'
reboot