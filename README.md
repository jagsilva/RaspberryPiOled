# RaspberryPiOled

## Experiencias com o OLED SH1106 no raspberry pi!




Criar o "virtual enviroment"

```
  python3 -m venv RPI-OLED-SH1106
```

Ativar o "virtual enviroment"

```
  source RPI-OLED-SH1106
```

Instalar o lib do oled

```
  pip3 install --upgrade luma.oled
```

Ativar o I2C para o utilizador, neste caso pi

```
  sudo usermod -a -G spi,gpio,i2c pi
```

Aceder à pasta do venv

```
  cd RPI-OLD-SH1106
```

Criar um exemplo para o oled

```
  sudo nano olaMundo.py
```

Conteudo do ficheiro:

```
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello World", fill="white")

# não terminar o script senão o display limpa e apaga
while(1):
	a=0
```
