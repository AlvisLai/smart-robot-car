import time


class Stepper:
    def __init__(self, pins, gpio):
        self.control_pins = pins
        self.GPIO = gpio
        self.step_seq_num = 0
        self.speed = 0.001
        self.rotate_dir = 1
        self.seq = [[1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1]]

    def setup(self):
        for pin in self.control_pins:
            self.GPIO.setup(pin, self.GPIO.OUT)
            self.GPIO.output(pin, False)

    def move(self, rotation):
        rotate = int(rotation * 4096)

        for i in range(0, (rotate + 1)):
            for pin in range(0, 4):
                pattern_pin = self.control_pins[pin]
                
                if self.seq[self.step_seq_num][pin] == 1:
                    self.GPIO.output(pattern_pin, True)
                else:
                    self.GPIO.output(pattern_pin, False)
                    
            self.step_seq_num += self.rotate_dir

            if (self.step_seq_num >= 8):
                self.step_seq_num = 0
                
            time.sleep(self.speed)