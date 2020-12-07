import time
import board
import digitalio
 
button = digitalio.DigitalInOut(board.D19)
button.switch_to_input(pull=digitalio.Pull.DOWN)
 
while True:
    if button.value:  # button is pushed
        print("On")
    else:
        print("Off")
 
    time.sleep(0.5)
