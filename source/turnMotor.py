from time import sleep
      
class turnMotor:
    def __init__(self, pins, gpio):
        self.control_pins = pins
        self.GPIO = gpio
        
    def setup(self):
        for pin in self.control_pins:
            self.GPIO.setup(pin, self.GPIO.OUT)
            self.GPIO.output(pin, True)
          
    def left(self):
        #true = turn off
        self.GPIO.output(20,True)
        self.GPIO.output(16,True)
        self.GPIO.output(24,False)
        self.GPIO.output(21,False)

    def right(self):
        #true = turn off
        self.GPIO.output(24,True)
        self.GPIO.output(21,True)
        self.GPIO.output(20,False)
        self.GPIO.output(16,False)

    def clear(self):
        for pin in self.control_pins:
            self.GPIO.output(pin,True)

    def turn(self, turnLeft):
        
        if(turnLeft):
            print("turn left")
            self.left()
        else:
            print("turn right")
            self.right()
        return
