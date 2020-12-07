import time
import board
import busio
import adafruit_pct2075 as pct2075
import adafruit_ssd1306 as ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
pct = pct2075.PCT2075(i2c)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x37)



while True:
    oled.fill(0)
    oled.text("Temp: %.2f C" %pct.temperature, 0, 0, 1)
    print("Temp: %.2f C" %pct.temperature)
    oled.show()
    time.sleep(0.5)
