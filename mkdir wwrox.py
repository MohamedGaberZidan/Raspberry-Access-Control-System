git clone https://github.com/MohamedGaberZidan/Raspberry-Access-Control-System.git
cd Raspberry-Access-Control-System
pip install -r requirements.txt
chmod u+x uninstall.sh
chmod u+x install.sh

# pip install --break-system-packages --user -r requirements.txt
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
@lxterminal -e python3 /home/zidan/Raspberry-Access-Control-System/qr.py > /tmp/output.txt & – Brian Agnew

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

cd /etc/xdg/lxsession/LXDE-pi/autostart
sudo autostart autostartback
sudo bash -c 'echo "@lxterminal -e python3 /home/zidan/Raspberry-Access-Control-System/qr.py">>autostart'
chmod 755





python setup.py uyaclpQvUul4VGsp 668f802e4c4e11ecb8029600000a0cbd



