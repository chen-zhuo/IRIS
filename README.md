## IRIS
IRIS (Indoor Route Instruction System) is a wearable device to provide in-building navigation guidance for a
visually-impaired person.

## Setting Up the Raspberry Pi

### Install Python 3.5.2
    cd ~
    wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
    tar -zxvf Python-3.5.2.tgz
    cd Python-3.5.2
    ./configure
    make
    sudo make install

### Configure the Raspberry Pi to Run a Python File Upon Boot
- Ensure that the boot option is set to “Console Autologin”, and “Wait for Network at Boot” is enabled.
    - In Terminal, enter `sudo raspi-config` to enter the configuration panel.
- Add autorun script to the “profile” file
    - In Terminal, enter `sudo nano /etc/profile`, and then append your script, for example:

        cd ~/Desktop/IRIS/
        sudo python3 ~/Desktop/IRIS/RaspberryPi/main.py



### Install mpg123 MP3 Player
    sudo apt-get update
    sudo apt-get install alsa-utils mpg123
    sudo reboot
    sudo modprobe snd_bcm2835
    sudo amixer cset numid=3 1
