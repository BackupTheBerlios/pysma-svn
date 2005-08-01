"""
World mesh agent for the prey/predator game.
"""
from pysma import Agent, Message
import random

random.seed()

class Mesh(Agent):
    def __init__(self, width, height):
        Agent.__init__(self)
        self.__width = width
        self.__height = height
        self.__world = [[None] * height for i in range(width)]
        
    def addAgent(self, agentId):
        case = -1
        while case != None:
            x = int(random.random() * self.__width)
            y = int(random.random() * self.__height)
            case = self.__world[x][y]
        self.__world[x][y] = agentId
        
    def born(self):
        self.requestRole(role="mover")
        
    def live(self):
        while self.hasMessage():
            msg = self.getNextMessage()
            if msg != None:
                direction = int(msg.content)
                x, y = (-1, -1)
                for i in range(self.__width):
                    for j in range(self.__height):
                        if self.__world[i][j] == msg.sender:
                            x, y = (i, j)
                if x != -1:
                    newX, newY = (-1, -1)
                    if direction == 0:
                        newX, newY = (x, (y-1)%self.__height)
                    elif direction == 1:
                        newX, newY = ((x+1)%self.__width, y)
                    elif direction == 2:
                        newX, newY = (x, (y+1)%self.__height)
                    elif direction == 3:
                        newX, newY = ((x-1)%self.__width, y)
                    if newX != -1:
                        if self.__world[newX][newY]==None:
                            self.__world[newX][newY] = msg.sender
                            self.__world[x][y] = None
                        else:
                            self.sendMessage(Message("NOT MOVED%s" %self.__world[newX][newY]), msg.sender)
        self.displayState_text()
        
    def displayState_text(self):
        lines = "-"*77+"\n"
        for i in range(self.__width):
            line = ""
            for j in range(self.__height):
                if self.__world[i][j] == None:
                    line = line + "[    ]\t"
                elif self.__world[i][j] in self.kernel.getAgentsWith(role="hunted"):
                    line = line + "[ ** ]\t"
                else:
                    line = line + "[ %02d ]\t" %self.__world[i][j]
            lines = lines + line + "\n"
        lines = lines + "-"*77
        print lines