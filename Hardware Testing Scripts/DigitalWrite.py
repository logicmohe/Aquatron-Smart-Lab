# Circuit Playground digitalio example
 
import time
import board
import digitalio
 
led = digitalio.DigitalInOut(board.D21)
led.switch_to_output(digitalio.Pull.DOWN)

 
while True:
    led.value = True
    #print("On")
    time.sleep(0.5)
    led.value = False
    #print("Off")
    time.sleep(0.5)