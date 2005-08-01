"""
Agent who can move in the world of the prey/predator game.
"""
from pysma import Agent, Message

class MovableAgent(Agent):
    direction = {"TOP":0, "RIGHT":1, "BOTTOM":2, "LEFT":3}
    
    def moveTo(self, aDirection):
        return self.sendBroadcastMessage(Message("%s" %aDirection), "mover")
