## IRIS
IRIS (Indoor Route Instruction System) is a wearable device to provide in-building navigation guidance for a
visually-impaired person.

## Setting Up the Raspberry Pi

### Install mpg123 MP3 Player
- `sudo apt-get update`
- `sudo apt-get install alsa-utils mpg123`
- `sudo reboot`
- `sudo modprobe snd_bcm2835`
- `sudo amixer cset numid=3 1`

Here the output is being set to 1, which is analog (headphone jack). Setting the output to 2 switches to HDMI. The
default setting is 0 which is automatic. To change the volume, enter

    amixer set PCM -- 85%

### Clone This Repository
- `cd ~/Desktop`
- `git clone https://github.com/chen-zhuo/IRIS.git`

### Configure the Raspberry Pi to Run a Python File Upon Boot
- Ensure that the boot option is set to “Console Autologin”, and “Wait for Network at Boot” is enabled.
    - In Terminal, enter `sudo raspi-config` to enter the configuration panel.
- Add autorun script to the “profile” file
    - In Terminal, enter `sudo nano /etc/profile`, and then append your script, for example:
        - `cd ~/Desktop/IRIS/RaspberryPi`
        - `python3 ~/Desktop/IRIS/RaspberryPi/main.py`

## References

### Text-To-Speech Audio Files Generator
- http://www.fromtexttospeech.com

### Raspberry Pi GPIO Pins
- https://www.raspberrypi.org/documentation/usage/gpio/
