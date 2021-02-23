import Jetson.GPIO as GPIO
import time


#pin_number is int, output value is like an enum (GPIO.LOW, GPIO.HIGH, etc)
def set_pin_output(pin_number, output_value, time):
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)
    # set pin as an output pin with optional initial state of the output value
    GPIO.setup(pin_number, GPIO.OUT, initial=output_value)

    print("Starting demo now! Press CTRL+C to exit")
    curr_value = output_value
    try:
        # Toggle the output every second
        print("Outputting {} to pin {}".format(curr_value, output_pin))
        GPIO.output(pin_number, curr_value)
        # this needs to be tested - atm i dont know if it will work
        curr_value ^= GPIO.HIGH
        time.sleep(time)
    finally:
        GPIO.cleanup()
