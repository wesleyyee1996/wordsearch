import time
import board
import digitalio
import pwmio
import keyboard

class StepperControl:
    def __init__(self):

        self.coil_A_blk_lr_pin = digitalio.DigitalInOut(board.D4)
        self.coil_C_grn_lr_pin = digitalio.DigitalInOut(board.D17)
        self.coil_B_red_lr_pin = digitalio.DigitalInOut(board.D24)
        self.coil_D_blu_lr_pin = digitalio.DigitalInOut(board.D23)
        self.coil_A_blk_ud_pin = digitalio.DigitalInOut(board.D10) #pin 19
        self.coil_C_grn_ud_pin = digitalio.DigitalInOut(board.D9) #pin 21
        self.coil_B_red_ud_pin = digitalio.DigitalInOut(board.D25) #pin 22
        self.coil_D_blu_ud_pin = digitalio.DigitalInOut(board.D8) #pin 24

        self.coil_A_blk_lr_pin.direction = digitalio.Direction.OUTPUT
        self.coil_C_grn_lr_pin.direction = digitalio.Direction.OUTPUT
        self.coil_B_red_lr_pin.direction = digitalio.Direction.OUTPUT
        self.coil_D_blu_lr_pin.direction = digitalio.Direction.OUTPUT
        self.coil_A_blk_ud_pin.direction = digitalio.Direction.OUTPUT
        self.coil_C_grn_ud_pin.direction = digitalio.Direction.OUTPUT
        self.coil_B_red_ud_pin.direction = digitalio.Direction.OUTPUT
        self.coil_D_blu_ud_pin.direction = digitalio.Direction.OUTPUT

        self.limit_y_2_pin = digitalio.DigitalInOut(board.D21) #pin 40
        self.limit_y_1_pin = digitalio.DigitalInOut(board.D20) #pin 38
        self.limit_x_1_pin = digitalio.DigitalInOut(board.D26) #pin 37
        self.limit_x_2_pin = digitalio.DigitalInOut(board.D19) #pin 35

        self.limit_y_1_pin.direction = digitalio.Direction.INPUT
        self.limit_y_2_pin.direction = digitalio.Direction.INPUT
        self.limit_x_1_pin.direction = digitalio.Direction.INPUT
        self.limit_x_2_pin.direction = digitalio.Direction.INPUT

        self.servo_pin = pwmio.PWMOut(board.D15, frequency=50) #pin 10

    def left(self,delay,steps):
        """
        delay: ms
        """
        delay = delay/1000.0
        i = 0
        while i in range(0, steps):
            if self.limit_x_1_pin.value:
                break
            self.setLRStep(1,1,0,0)
            time.sleep(delay)
            self.setLRStep(0,1,1,0)
            time.sleep(delay)
            self.setLRStep(0,0,1,1)
            time.sleep(delay)
            self.setLRStep(1,0,0,1)
            time.sleep(delay)
            i += 1
        self.setLRStep(0,0,0,0)
        return i

    def right(self,delay,steps):
        i = 0
        delay = delay/1000.0
        while i in range(0, steps):   
            if self.limit_x_2_pin.value:
                break
            self.setLRStep(1,0,0,1)
            time.sleep(delay)
            self.setLRStep(0,0,1,1)
            time.sleep(delay)
            self.setLRStep(0,1,1,0)
            time.sleep(delay)
            self.setLRStep(1,1,0,0)
            time.sleep(delay)
            i += 1
        self.setLRStep(0,0,0,0)
        return i

    def down(self,delay,steps):
        i = 0
        delay = delay/1000.0
        while i in range(0, steps):
            if self.limit_y_2_pin.value:
                break
            self.setUDStep(1,1,0,0)
            time.sleep(delay)
            self.setUDStep(0,1,1,0)
            time.sleep(delay)
            self.setUDStep(0,0,1,1)
            time.sleep(delay)
            self.setUDStep(1,0,0,1)
            time.sleep(delay)
            i += 1

        self.setUDStep(0,0,0,0)
        return i

    def up(self,delay,steps):
        i = 0
        delay = delay/1000.0
        while i in range(0, steps): 
            if self.limit_y_1_pin.value:
                break
            self.setUDStep(1,0,0,1)
            time.sleep(delay)
            self.setUDStep(0,0,1,1)
            time.sleep(delay)
            self.setUDStep(0,1,1,0)
            time.sleep(delay)
            self.setUDStep(1,1,0,0)
            time.sleep(delay)
            i += 1
        self.setUDStep(0,0,0,0)
        return i

    def setLRStep(self, A, B, C, D):
        self.coil_A_blk_lr_pin.value = A
        self.coil_C_grn_lr_pin.value = C
        self.coil_B_red_lr_pin.value = B
        self.coil_D_blu_lr_pin.value = D

    def setUDStep(self, A, B, C, D):
        self.coil_A_blk_ud_pin.value = A
        self.coil_C_grn_ud_pin.value = C
        self.coil_B_red_ud_pin.value = B
        self.coil_D_blu_ud_pin.value = D

    def servo(self, duty):
        self.servo_pin.duty_cycle = duty*65535/100

"""
user_delay = 1
user_steps = 50

stepper = StepperControl()

def kbdCallback(e):
    key = keyboard.normalize_name(e.name)
    if key == "left":
        stepper.left(1/1000.0, 30)
        print("left")
    elif key == "right":
        stepper.right(1/1000.0,30)
        print("right")
    elif key == "up":
        stepper.up(1/1000.0,30)
        print("up")
    elif key == "down":
        stepper.down(1/1000.0,30)
        print("up")
    else:
        stepper.setLRStep(0,0,0,0)
        stepper.setUDStep(0,0,0,0)
        print("stopped")

keyboard.on_press(kbdCallback)

while True:
    time.sleep(1)
"""
"""
while True:
    setStep(0,0,0,0)
    #user_delay = input("Delay b/w steps (ms):")
    #user_steps = input("Number of steps forward:")
    forward(float(user_delay) / 1000.0, int(user_steps))
    setStep(0,0,0,0)
    time.sleep(1)
    #user_steps = input("Number of steps backward:")
    backwards(float(user_delay) / 1000.0, int(user_steps))
    setStep(0,0,0,0)
    time.sleep(1)
"""
