#/usr/bin/python

from stepper_control import StepperControl
import threading

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+self.x+","+self.y+")"

class Move:
    def __init__(self):
        self.stepper = StepperControl()

        self.step_freq = 1.4
        self.ud_max_steps = 198
        self.lr_max_steps = 108

        self.x = 0
        self.y = 0
        
        self.home()

    def home(self):
        self.stepper.down(self.step_freq, 300)           
        self.stepper.up(self.step_freq, 5)

        self.stepper.left(self.step_freq, 200)
        self.stepper.right(self.step_freq, 5)

    def calibrate(self):
        ud_steps = self.stepper.up(self.step_freq, 300)
        self.stepper.down(self.step_freq, 5)
        self.ud_max_steps = ud_steps - 5

        lr_steps = self.stepper.right(self.step_freq, 200)
        self.stepper.left(self.step_freq, 5)
        self.lr_max_steps = lr_steps - 5

    def move_x(self, x_amt):
        if x_amt > 0:
            self.stepper.right(self.step_freq, x_amt)
        else:
            self.stepper.left(self.step_freq, x_amt)

    def move_y(self, y_amt):
        if y_amt> 0:
            self.stepper.up(self.step_freq, y_amt)
        else:
            self.stepper.down(self.step_freq, y_amt)

    def to(self, position):
        """
        Moves to a certain position
        """
        
        position.x = min(self.lr_max_steps, position.x)
        position.x = max(position.x, 0)
        position.y = min(self.ud_max_steps, position.y)
        position.y = max(position.y, 0)

        vec_x = position.x - self.x
        vec_y = position.y - self.y

        self.move_x(vec_x)
        self.move_y(vec_y)

        """
        t1 = threading.Thread(target = self.move_x, args = [vec_x])
        t2 = threading.Thread(target = self.move_y, args = [vec_y])

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        """

        self.x = position.x
        self.y = position.y



if __name__ == '__main__':

    try:
        move = Move()
        
        #move.calibrate()

        while True:
            _x = input("X:")
            _y = input("Y:")
            move.to(Point(int(_x),int(_y)))



    except KeyboardInterrupt:
        move.stepper.setUDStep(0,0,0,0)
        move.stepper.setLRStep(0,0,0,0)


"""
import digitalio
import board
import time

limity1 = digitalio.DigitalInOut(board.D21) #pin 40
limity1.direction = digitalio.Direction.INPUT
limity2 = digitalio.DigitalInOut(board.D20) #pin 38
limity2.direction = digitalio.Direction.INPUT

while True:
    time.sleep(0.1)
    print("Y1",limity1.value)
    print("Y2",limity2.value)
"""
