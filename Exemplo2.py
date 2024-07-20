from luma.core.serial import i2c
from luma.core.render import canvas

from luma.oled.device import sh1106

def do_nothing(obj):
    pass

serial = i2c(port=0)
device = sh1106(serial)

# override the cleanup method
device.cleanup = do_nothing

hostname = "OrangePi Zero"
ip = "192.11.23.191"

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, fill="black", outline="white")
    draw.text((3, 2), hostname, fill="white")
    draw.text((3, 12), ip, fill="white")
