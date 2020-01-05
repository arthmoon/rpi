cd /home/pi
git clone https://github.com/arthmoon/rpi.git
cp /home/pi/rpi/water.py /home/pi/rpi/sync.py /home/pi/rpi/sync.sh /home/pi/rpi/tmp /home/pi/
sudo chown pi:pi /home/pi/sync.py /home/pi/sync.sh /home/pi/water.py
sudo chmod +x /home/pi/sync.sh
cp /home/pi/rpi/water.rules /etc/udev/rules.d/
sudo cp /home/pi/rpi/water.desktop /etc/xdg/autostart/
crontab /home/pi/rpi/crontab.txt