"""
Predator agent of the prey/predator game.
"""
from movableAgent import MovableAgent
import random

random.seed()

class Predator(MovableAgent):
    def born(self):
        self.requestRole(role="hunter")
    
    def live(self):
        direction = int(random.random() * 4)
        self.moveTo(direction)
