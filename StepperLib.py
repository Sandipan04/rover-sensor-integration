'''
Controlling a stepper motor using the A4988 driver.
'''
from time import sleep

class Stepper():
    def __init__(self, total_steps, board, dir_pin, step_pin, micro_step_pins=(0,0,0)):

        # initializes the pins as outputs
        self.dir_pin = board.get_pin(f'd:{dir_pin}:o')
        self.step_pin = board.get_pin(f'd:{step_pin}:o')
        self.micro_step_pins = [
            board.get_pin(f'd:{micro_step_pins[0]}:o'),
            board.get_pin(f'd:{micro_step_pins[1]}:o'),
            board.get_pin(f'd:{micro_step_pins[2]}:o'),
        ]

        self.step_number = 0 # what number of steps are going to be turned
        self.direction = 0
        self.total_steps = total_steps # total number of steps per revolution
        self.step_delay = 0 # time delay between steps

    def switch_direction(self):
        self.direction = 1 if self.direction == 0 else 0
    
    def turn_angle(self, degrees):
        if degrees < 0:
            self.switch_direction()
            degrees = -degrees
            
        steps_to_move = (degrees*self.total_steps)/360
        step_sizes = [360/(200*2**x) for x in range(0,5)] # in degrees

        for i, step_size in enumerate(step_sizes):
            self.set_resolution(i)
            self.step(steps_to_move//step_size)

            print(f'1/{2**(i)} steps: {steps_to_move//step_size}')
            steps_to_move = round(steps_to_move%step_size, 4)
            print('remaining steps', steps_to_move)
            print()

        print('remaining angle:', steps_to_move*1.8)

    def step(self, steps):
        for i in range(steps):
            self.step_pin.write(1)
            sleep(self.step_delay)
            self.step_pin.write(0)
            sleep(self.step_delay)
            
            print(i)
        # self.step_pin.write(0)

    def set_resolution(self, resolution):
        '''
        Defined resolutions: 1, 1/2, 1/4, 1/8, 1/16 indexed from [0, 4]
        '''
        if resolution == 0: # full step
            states = (0, 0, 0)
        elif resolution == 1: # half step
            states = (1, 0, 0)
        elif resolution == 2: # quarter step
            states = (0, 1, 0)    
        elif resolution == 3: # 1/8th step
            states = (1, 1, 0)
        elif resolution == 4: # 1/16th step
            states = (1, 1, 1)

        for pin, state in zip(self.micro_step_pins, states):
            pin.write(state)
