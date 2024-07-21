#!/home/pi/RPI-OLED-SH1106/bin/python


#blog.berrybase.de


from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image

import time
import psutil
import socket

from datetime import datetime

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

#oled_font = ImageFont.truetype('arial.ttf', 12)

while True:

    hostname = socket.gethostname() 

    #Calculate memory information
    memory = psutil.virtual_memory()
    #Convert Bytes to MB (Bytes -> KB -> MB)
    available = round(memory.available/1024.0/1024.0/1024.0,1)
    totalm = round(memory.total/1024.0/1024.0/1024.0,1)
    mem_info = str(available) + 'GB free / ' + str(totalm) + 'GB total ( ' + str(memory.percent) + '% )'

    # Calculate disk information
    disk = psutil.disk_usage('/')
    # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    totald = round(disk.total/1024.0/1024.0/1024.0,1)
    disk_info = str(free) + 'GB free / ' + str(totald) + 'GB total ( ' + str(disk.percent) + '% )'

    temp = int(psutil.sensors_temperatures()['cpu_thermal'][0].current)

    uptime_sec =  time.time() - psutil.boot_time()

    boot_time_timestamp = psutil.boot_time()
    current_time_timestamp = time.time()
    uptime_seconds = current_time_timestamp - boot_time_timestamp
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
#    uptime_str = f"{int(uptime_days)} days, {int(uptime_hours % 24)} hours, {int(uptime_minutes % 60)} minutes, {int(uptime_seconds % 60)} seconds"
    uptime_str = f"{int(uptime_days)} D, {int(uptime_hours % 24)}H {int(uptime_minutes % 60)}M"




    with canvas(device) as draw:
        draw.text((10, 1 ),hostname,  fill = "white")
        draw.text((1, 13),"RAM LIVRE :   " + str(available) + " / " + str(totalm) + " GB" ,  fill = "white")
        draw.text((1, 25),"SD LIVRE  :   " + str(free)      + " / " + str(totald) + " GB" ,  fill = "white")
        draw.text((1, 38),str(datetime.now().strftime('%d.%m.%Y     %H:%M:%S')) ,  fill = "white")
        draw.text((1, 50),str(temp) + " C" ,  fill = "white")
        draw.text((50, 50),uptime_str ,  fill = "white")
    time.sleep(5)
