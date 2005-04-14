"""
Prey agent of the prey/predator game.
"""
from movableAgent import MovableAgent
from pysma import kernel
import random

random.seed()

class Prey(MovableAgent):
    def born(self):
        self.requestRole(role="hunted")
    
    def live(self):
        if (self.hasMessage()):
            msg = self.getNextMessage()
            if msg.content[:9] == "NOT MOVED":
                print "The prey has been catched by Agent #%s !!!" %msg.content[9:]
                self.kernel.stopKernel()
                return
        direction = int(random.random() * 40) / 10
        self.moveTo(direction)
