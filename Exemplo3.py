# -*- coding:UTF-8 -*-

from luma.core.interface.serial import i2c
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

def getHostIp():
    try:
        my = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my.connect(('8.8.8.8', 80))
        # ip = my.getsockname()[0]
        ipList = my.getsockname()
    finally:
        my.close()
    return ipList

# Return % of CPU used by user as a character string
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))

# Return CPU temperature as a character string
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])


def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def ramTotal():
    return(round(int(getRAMinfo()[0]) / 1000,1))

def ramUsed():
    return(round(int(getRAMinfo()[1]) / 1000,1))

def ramFree():
    return(round(int(getRAMinfo()[3]) / 1000,1))

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







ipaddr = get_ip()

print (ipaddr)

#with canvas(device) as draw:
#    draw.rectangle(device.bounding_box, fill="black", outline="white")
#    draw.text((3, 12), hostname, fill="white")
#    draw.text((3, 22), ipaddr, fill="white")


while True:
       with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((18, 5), "Hshen raspberry" , fill="white")
            draw.text((2, 14), " CPU: " + getCPUuse() , fill="white")
            draw.text((62, 14), " Temp: " + getCPUtemperature() , fill="white")
            draw.text((2, 23), " RAM: " + str(ramUsed()) + "/" + str(ramTotal()) , fill="white")
            draw.text((2, 33), " Disco: " + str(getDiskSpace()[1]) + " / " + str(getDiskSpace()[0]) , fill="white")
            draw.text((2, 42), " IP:" + getHostIp()[0] , fill="white")
            draw.text((2, 52),time.strftime("    %d-%m-%Y %H:%M", time.localtime())  , fill="white")
       time.sleep(2)
