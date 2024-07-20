rom luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

import socket
import time
import os
import psutil
import platform
from datetime import datetime

def do_nothing(obj):
    pass

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# override the cleanup method
device.cleanup = do_nothing

hostname = "RPI4 4GB"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

byteunits = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
def filesizeformat(value):
    exponent = int(log(value, 1024))
    return "%.1f %s" % (float(value) / pow(1024, exponent), byteunits[exponent])

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


def cpu_usage():
    # load average, uptime
    av1, av2, av3 = os.getloadavg()
    return "%.1f %.1f %.1f" \
        % (av1, av2, av3)

def cpu_temperature():
    tempC = ((int(open('/sys/class/thermal/thermal_zone0/temp').read())))
    return "%sc" \
        % (str(tempC))

def mem_usage():
    usage = psutil.virtual_memory()
    return "%s/%s" \
        % (bytes2human(usage.available), bytes2human(usage.total))

def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return " %s/%s" \
        % (bytes2human(usage.total-usage.used), bytes2human(usage.total))

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def lan_ip():
    #f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -c 21-33')
    f = os.popen("ip route get 1 | awk '{print $NF;exit}'")
    ip = str(f.read())
    # strip out trailing chars for cleaner output
    return "%s" % ip.rstrip('\r\n').rstrip(' ')

Normal = '\033[0m'

# High Intensity
IGreen='\033[0;92m'       # Green
IYellow='\033[0;93m'      # Yellow
IBlue='\033[0;94m'        # Blue
ICyan='\033[0;96m'        # Cyan
IWhite='\033[0;97m'       # White

# Bold High Intensity
BIRed='\033[1;91m'        # Red
BIGreen='\033[1;92m'      # Green
BIYellow='\033[1;93m'     # Yellow
BIPurple='\033[1;95m'     # Purple
BIMagenta='\033[1;95m'    # Purple
BICyan='\033[1;96m'       # Cyan
BIWhite='\033[1;97m'      # White

uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

os.system('cls' if os.name == 'nt' else 'clear')
print (IBlue + "____________________________________________________________________________\n" + Normal )
print (" Platform: " + BIPurple + "%s" % (platform.platform()) + Normal )
print (" CPU Usage: " + BIRed + cpu_usage() + Normal + "\t\tCPU Temperature: " + BIRed + cpu_temperature() + Normal )
print (" Memory Free: " + BIRed + mem_usage() + Normal + "\t\tDisk Free: " + BIRed + disk_usage('/') + Normal )
print (" IP Address: " + BIRed + lan_ip() + Normal + "\tUptime: " + BIRed + "%s" % str(uptime).split('.')[0]  + Normal )
bum=psutil.cpu_freq(0)
#print " Current CPU speed: " + BIRed + "%d" % int(bum.current) + "Mhz" + Normal + "\tmin: " + BIRed + "%d" % int(bum.min) + "Mhz" + Normal + " max: " + BIRed + "%d" % int(bum.max) + "Mhz" + Normal
#print " Time/Date: " + IGreen + str(datetime.now().strftime('%a %b %d at %H:%M:%S')) + Normal
print (" Current CPU speed: " + BIRed + "%d" % int(bum.current) + "Mhz" + Normal + "\t" + IGreen + str(datetime.now().strftime('%a %b %d at %H:%M:%S')) + Normal)
print (IBlue + "____________________________________________________________________________\n" + Normal)
